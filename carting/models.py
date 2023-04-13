from __future__ import annotations

import logging
from enum import Enum
from functools import cached_property
from typing import Iterator, NamedTuple
from xml.etree import ElementTree

import lxml.etree as ET
from django.contrib.gis.db import models
from django.db import DatabaseError
from django.utils.safestring import mark_safe
from tree_queries.models import TreeNode, TreeQuerySet
from xmlschema import etree_tostring

xslt_transform = ET.XSLT(ET.parse("carting/xslt/ouvrage_section_html.xslt"))


class SectionIngester(NamedTuple):
    element: ElementTree.Element
    ouvrage_name: str

    def numero(self, parent: OuvrageSection) -> str:
        return parent.numero

    def content(self) -> str:
        return ElementTree.tostring(self.element, encoding="unicode")


class AlineaIngester(SectionIngester):
    def numero(self, parent: OuvrageSection) -> str:
        return f"{parent.numero}0.{self.element.find('nmrAlinea').text}"


class FigureIngester(SectionIngester):
    def numero(self, parent: OuvrageSection) -> str:
        return self.element.find("numero").text


class ParagraphIngester(SectionIngester):
    def numero(self, parent: OuvrageSection) -> str:
        return self.element.find("titre/numero").text

    def content(self) -> str:
        return ElementTree.tostring(self.element.find("titre"), encoding="unicode")


class OuvrageIngester(SectionIngester):
    def numero(self, parent: None) -> str:
        return self.ouvrage_name

    def content(self) -> str:
        return ""


class SectionTypology(Enum):
    _ignore_ = "Definition"

    class Definition(NamedTuple):
        xpaths: list[str]
        ingester: type[SectionIngester]
        html_tag: str | None = None

    OUVRAGE = Definition(["ouvrage"], OuvrageIngester)
    CHAPTER = Definition(["chapitre"], ParagraphIngester, "h2")
    SUBCHAPTER = Definition(["sChapitre"], ParagraphIngester, "h3")
    PARAGRAPH = Definition(["para"], ParagraphIngester, "h4")
    SUBPARAGRAPH = Definition(["sPara"], ParagraphIngester, "h5")
    SUBSUBPARAGRAPH = Definition(["ssPara"], ParagraphIngester, "h6")
    ALINEA = Definition(["alinea"], AlineaIngester)
    TABLE = Definition(["tableau"], FigureIngester)
    ILLUSTRATION = Definition(["illustration"], FigureIngester)
    TOPONYME = Definition(["texte/principal", "liste/texte/principal"], SectionIngester)
    REFERENCE = Definition(
        ["texte/reference", "liste/texte/reference"], SectionIngester
    )

    @property
    def label(self) -> str:
        return self.name.capitalize()

    @property
    def xpaths(self) -> list[str]:
        return self.value.xpaths

    @property
    def html_tag(self) -> str:
        return self.value.html_tag

    @property
    def ingester(self) -> type[SectionIngester]:
        return self.value.ingester

    @classmethod
    @property
    def choices(cls) -> list[tuple[str, str]]:
        return [(member.name, member.label) for member in cls]


def find_ingestable_child_elements(
    element: ElementTree.Element,
) -> Iterator[tuple[SectionTypology, ElementTree.Element]]:
    for typology in SectionTypology:
        for xpath in typology.xpaths:
            for child_element in element.iterfind(xpath):
                yield typology, child_element


class OuvrageSectionManager(models.Manager):
    def ingest_xml_subtree(
        self,
        ouvrage_name: str,
        element: ElementTree.Element,
        ouvrage_section: OuvrageSection | None = None,
    ) -> int:
        ingested = 0
        for typology, child_element in find_ingestable_child_elements(element):
            child_ouvrage_section = OuvrageSection.from_xml(
                child_element, ouvrage_section, typology, ouvrage_name
            )
            child_ouvrage_section.ingest()

            logging.info(
                "Section %s ingérée avec l'id %s",
                typology.name,
                child_ouvrage_section.bpn_id,
            )
            ingested += 1
            ingested += self.ingest_xml_subtree(
                ouvrage_name, child_element, child_ouvrage_section
            )
        return ingested


class OuvrageSection(TreeNode):
    objects = OuvrageSectionManager.from_queryset(TreeQuerySet)()

    bpn_id = models.UUIDField(primary_key=True)
    numero = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    typology = models.CharField(max_length=25, choices=SectionTypology.choices)
    ouvrage_name = models.CharField(max_length=10)
    geometry = models.GeometryField(blank=True, null=True, default=None, srid=4326)

    class Meta:
        ordering = ("numero",)

    def __str__(self):
        return f"{self.numero} - {self.typology_object.label}"

    @property
    def typology_object(self) -> SectionTypology:
        return SectionTypology[self.typology]

    @classmethod
    def from_xml(
        cls,
        element: ElementTree.Element,
        parent: "OuvrageSection" | None,
        typology: SectionTypology,
        ouvrage_name: str,
    ) -> "OuvrageSection":
        ingester = typology.ingester(element, ouvrage_name)

        return cls(
            bpn_id=element.attrib["bpn_id"],
            numero=ingester.numero(parent),
            content=ingester.content(),
            typology=typology.name,
            ouvrage_name=ouvrage_name,
            parent=parent,
        )

    def ingest(self):
        self.clean_fields()

        try:
            # This raises if the instance does not exist
            self.save(
                update_fields=(
                    "numero",
                    "content",
                    "typology",
                    "ouvrage_name",
                    "parent",
                )
            )
        except DatabaseError:
            self.save()

    @cached_property
    def content_html(self):
        if not self.content:
            return ""

        inner_html = xslt_transform(ET.fromstring(self.content))

        html_tag = self.typology_object.html_tag

        if html_tag:
            # FIXME : extraire dans un templatetag django
            inner_html = f'<{html_tag} class="fr-mt-2w">{inner_html}</{html_tag}>'
        return mark_safe(inner_html)

    @property
    def should_display(self):
        return self.typology_object not in [
            SectionTypology.REFERENCE,
            SectionTypology.TOPONYME,
        ]


from django.contrib.gis.geos import GEOSGeometry
from lxml import etree


def get_submember2(root):
    member = root.find("member") or root.find("imember")
    return member[0]


class S1xyObject(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    typology = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    geometry = models.GeometryField(blank=True, null=True, default=None, srid=4326)
    link_to = models.ManyToManyField("self", blank=True)

    def _create_links(self):
        for link_id in self._collect_link_ids():
            (link_obj, _) = S1xyObject.objects.get_or_create(id=link_id)
            self.link_to.add(link_obj)

    def _get_submember(self):
        root = etree.fromstring(self.content)
        return get_submember2(root)

    @classmethod
    def inject_from_xml_str(cls, xml_str: str):
        root = etree.fromstring(xml_str)
        sub_member = get_submember2(root)
        gml_id = sub_member.get("{" + sub_member.nsmap["gml"] + "}id")
        typology = sub_member.prefix + ":" + etree.QName(sub_member).localname

        geometry = None
        geom = sub_member.find("geometry")
        if geom is not None:
            try:
                geometry = GEOSGeometry.from_gml(
                    etree.tostring(geom[0][0], method="xml", encoding="unicode")
                )
            except IndexError:
                pass

        (s1xy_object, _) = S1xyObject.objects.update_or_create(
            id=gml_id,
            defaults={
                "typology": typology,
                "content": xml_str,
                "geometry": geometry,
            },
        )
        s1xy_object._create_links()
        return s1xy_object

    def _collect_link_ids(self):
        sub_member = self._get_submember()
        to_link_list = []
        for child in sub_member.findall(
            ".//*[@{" + sub_member.nsmap["xlink"] + "}href]"
        ):
            child_href = child.get("{" + child.nsmap["xlink"] + "}href")
            child_href = child_href.replace("#", "")
            to_link_list.append(child_href)
        return to_link_list
