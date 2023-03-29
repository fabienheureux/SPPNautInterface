import json
import time
from uuid import UUID

import requests
from django.contrib.gis import geos
from django.core import serializers
from django.core.serializers import serialize
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from carting.models import OuvrageSection, SectionTypology

GeoJSONSerializer = serializers.get_serializer("geojson")


# Remove if on Django 4.2 https://github.com/django/django/pull/15740
# https://stackoverflow.com/questions/34556679/geodjango-serialize-geojson-skipping-id-field
class Serializer(GeoJSONSerializer):
    def get_dump_object(self, obj):
        data = super().get_dump_object(obj)
        data.update(id=obj.pk)
        return data


@require_GET
def geometry_first(request: HttpRequest) -> HttpResponse:
    # time.sleep(0.5)
    qs_bbox = request.GET.get(
        "bbox",
        "-3.1544249873003865, 47.32998953301873, -1.6582899424738569, 49.140572742794404",
    )
    # FIXME: Meilleur cast
    zoom_level = int(float(request.GET.get("zoom", 1)))
    expanded = request.GET.get("expanded")

    qs_bbox = [float(coordinate) for coordinate in qs_bbox.split(",")]
    bbox = geos.Polygon.from_bbox(qs_bbox)
    sections = (
        OuvrageSection.objects.filter(geometry__bboverlaps=bbox)
        # FIXME : A geometry is not excluded by filter below 75f7dbbd-c0b4-456f-bc10-19f72f89608b
        .exclude(geometry__contains_properly=bbox).exclude(
            # .exclude(
            typology__in=[
                SectionTypology.ILLUSTRATION.name,
                SectionTypology.OUVRAGE.name,
                SectionTypology.TABLE.name,
                SectionTypology.TOPONYME.name,
                SectionTypology.REFERENCE.name,
                SectionTypology.ALINEA.name,
            ]
        )
    )
    # .descendants(include_self=True)
    if zoom_level < 7:
        sections = sections.filter(typology__in=[SectionTypology.CHAPTER.name])

    from pathlib import Path

    Path("debug.sql").write_text(
        sections.explain(
            analyze=True, buffers=True, verbose=True, settings=True, wal=True
        )
    )
    expanded_section = None
    if expanded:
        # expanded_section = OuvrageSection.objects.get(pk=expanded).descendants(
        #     include_self=True
        # )
        expanded_section = OuvrageSection.objects.prefetch_related("children").get(
            pk=expanded
        )
        # expanded_section = expanded_section.descendants(include_self=True)

    to_serialize = sections
    if expanded_section:
        to_serialize = [expanded_section, *expanded_section.children.all()]
    geojson = Serializer().serialize(s for s in to_serialize if s.geometry)

    if root_expanded := request.GET.get("root_expanded"):
        root_expanded = UUID(root_expanded)
    return render(
        request,
        "carting/geometry_first.html",
        {
            "scroll_snap": True,
            "geojson": geojson,
            "bbox": json.dumps(qs_bbox),
            "zoom_level": zoom_level,
            "sections": sections,
            "root_expanded": root_expanded,
            "expanded_section": expanded_section,
        },
    )


# FIXME : Les sections commençant par '0.' ne devraient pas être affichées (pas de géométrie attachée); les illustrations en '0.' sont mal ordonnées
@require_GET
def text_first(request: HttpRequest) -> HttpResponse:
    search = request.GET.get("search", "")

    if not search:
        return redirect(reverse("carting:text_first") + "?search=4.1.")

    if not search.endswith("."):
        return redirect(reverse("carting:text_first") + f"?search={search}.")

    ouvrage, _, numero = search.rpartition("/")
    if not numero:
        return render(
            request,
            "carting/text_first.html",
        )

    sections = OuvrageSection.objects.exclude(
        typology__in=[
            SectionTypology.ALINEA.name,
            SectionTypology.ILLUSTRATION.name,
            SectionTypology.REFERENCE.name,
            SectionTypology.TABLE.name,
            SectionTypology.TOPONYME.name,
        ]
    ).with_tree_fields()
    if ouvrage:
        sections = sections.filter(ouvrage_name=ouvrage)
    try:
        # FIXME: 4.2. get() returned more than one OuvrageSection -- it returned 2!
        section = sections.get(numero=numero)
    except OuvrageSection.DoesNotExist:
        raise Http404(
            "Probably we won't fix it : No OuvrageSection matches the given query."
        )
    except OuvrageSection.MultipleObjectsReturned:
        raise Http404(
            "Probably we won't fix it : Multiple OuvrageSections match the given query."
        )
    sections = [*section.ancestors(), *section.descendants(include_self=True)]

    geojson = Serializer().serialize(s for s in sections if s.geometry)

    return render(
        request,
        "carting/text_first.html",
        {
            "sections": sections,
            "geojson": geojson,
            "search_tree_depth": section.tree_depth,
            "search": search,
        },
    )


# Needed until https://github.com/betagouv/SPPNautInterface/issues/185 is closed
@require_GET
def wms_proxy(request, wms_url):
    response = requests.get(url=wms_url, params=request.GET.dict())
    http_response = HttpResponse(response)
    headers_to_forward = ["Content-Type", "Content-Length"]
    for header in headers_to_forward:
        if header in response.headers:
            http_response.headers[header] = response.headers[header]
    return http_response
