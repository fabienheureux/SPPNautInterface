import copy

from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from lxml import etree

from carting.models import S1xyObject


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "filepath",
            type=str,
            help="filepath to S1xy.xml file",
        )

    def handle(self, *args, **options):
        S1xyObject.objects.all().delete()

        filepath = options.get("filepath")
        tree = etree.parse(filepath)
        root = tree.getroot()

        object_root = copy.deepcopy(root)
        etree.strip_elements(object_root, "member", "imember")

        for member in ("member", "imember"):
            for object in root.findall(member):
                object_content = copy.deepcopy(object_root)
                object_content.append(object)
                object_xml = etree.tostring(
                    object_content, method="xml", encoding="unicode"
                )
                S1xyObject.inject_from_xml_str(object_xml)
