# Generated by Django 4.1.7 on 2023-05-09 10:03

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import s100.models
import s127.models.organisation_contact_area
import s127.models.shared


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Applicability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "in_ballast",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Yes"), (False, "No")],
                        help_text="Whether the vessel is in ballast.",
                        null=True,
                    ),
                ),
                (
                    "category_of_cargo",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("bulk", "Bulk"),
                                ("container", "Container"),
                                ("general", "General"),
                                ("liquid", "Liquid"),
                                ("passenger", "Passenger"),
                                ("livestock", "Livestock"),
                                ("dangerous or hazardous", "Dangerous Or Hazardous"),
                                ("heavy lift", "Heavy Lift"),
                                ("ballast", "Ballast"),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Classification of the different types of cargo that a ship may be carrying",
                        size=None,
                    ),
                ),
                (
                    "category_of_dangerous_or_hazardous_cargo",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                (
                                    "IMDG Code Class 1 Div. 1.1",
                                    "Imdg Code Class 1 Div 1 1",
                                ),
                                (
                                    "IMDG Code Class 1 Div. 1.2",
                                    "Imdg Code Class 1 Div 1 2",
                                ),
                                (
                                    "IMDG Code Class 1 Div. 1.3",
                                    "Imdg Code Class 1 Div 1 3",
                                ),
                                (
                                    "IMDG Code Class 1 Div. 1.4",
                                    "Imdg Code Class 1 Div 1 4",
                                ),
                                (
                                    "IMDG Code Class 1 Div. 1.5",
                                    "Imdg Code Class 1 Div 1 5",
                                ),
                                (
                                    "IMDG Code Class 1 Div. 1.6",
                                    "Imdg Code Class 1 Div 1 6",
                                ),
                                (
                                    "IMDG Code Class 2 Div. 2.1",
                                    "Imdg Code Class 2 Div 2 1",
                                ),
                                (
                                    "IMDG Code Class 2 Div. 2.2",
                                    "Imdg Code Class 2 Div 2 2",
                                ),
                                (
                                    "IMDG Code Class 2 Div. 2.3",
                                    "Imdg Code Class 2 Div 2 3",
                                ),
                                ("IMDG Code Class 3", "Imdg Code Class 3"),
                                (
                                    "IMDG Code Class 4 Div. 4.1",
                                    "Imdg Code Class 4 Div 4 1",
                                ),
                                (
                                    "IMDG Code Class 4 Div. 4.2",
                                    "Imdg Code Class 4 Div 4 2",
                                ),
                                (
                                    "IMDG Code Class 4 Div. 4.3",
                                    "Imdg Code Class 4 Div 4 3",
                                ),
                                (
                                    "IMDG Code Class 5 Div. 5.1",
                                    "Imdg Code Class 5 Div 5 1",
                                ),
                                (
                                    "IMDG Code Class 5 Div. 5.2",
                                    "Imdg Code Class 5 Div 5 2",
                                ),
                                (
                                    "IMDG Code Class 6 Div. 6.1",
                                    "Imdg Code Class 6 Div 6 1",
                                ),
                                (
                                    "IMDG Code Class 6 Div. 6.2",
                                    "Imdg Code Class 6 Div 6 2",
                                ),
                                ("IMDG Code Class 7", "Imdg Code Class 7"),
                                ("IMDG Code Class 8", "Imdg Code Class 8"),
                                ("IMDG Code Class 9", "Imdg Code Class 9"),
                                (
                                    "Harmful Substances in packaged form",
                                    "Harmful Substances In Packaged Form",
                                ),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Classification of dangerous goods or hazardous materials based on the International Maritime Dangerous Goods Code (<a href='https://www.imo.org/fr/OurWork/Safety/Pages/DangerousGoods-default.aspx' target='_blank'>IMDG Code</a>)",
                        size=None,
                    ),
                ),
                (
                    "category_of_vessel",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("general cargo vessel", "General Cargo Vessel"),
                            ("container carrier", "Container Carrier"),
                            ("tanker", "Tanker"),
                            ("bulk carrier", "Bulk Carrier"),
                            ("passenger vessel", "Passenger Vessel"),
                            ("roll-on roll-off", "Roll On Roll Off"),
                            ("refrigerated cargo vessel", "Refrigerated Cargo Vessel"),
                            ("fishing vessel", "Fishing Vessel"),
                            ("service", "Service"),
                            ("warship", "Warship"),
                            (
                                "towed or pushed composite unit",
                                "Towed Or Pushed Composite Unit",
                            ),
                            ("tug and tow", "Tug And Tow"),
                            ("light recreational", "Light Recreational"),
                            (
                                "semi-submersible offshore installation",
                                "Semi Submersible Offshore Installation",
                            ),
                            (
                                "jackup exploration or project installation",
                                "Jackup Exploration Or Project Installation",
                            ),
                            ("livestock carrier", "Livestock Carrier"),
                            ("sport fishing", "Sport Fishing"),
                        ],
                        help_text="Classification of vessels by function or use",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category_of_vessel_registry",
                    models.CharField(
                        blank=True,
                        choices=[("domestic", "Domestic"), ("foreign", "Foreign")],
                        help_text="The locality of vessel registration or enrolment relative to the nationality of a port, territorial sea, administrative area, exclusive zone or other location.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "logical_connectives",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("logical conjunction", "Logical Conjunction"),
                            ("logical disjunction", "Logical Disjunction"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "thickness_of_ice_capability",
                    models.IntegerField(
                        blank=True,
                        help_text="The thickness of ice that the ship can safely transit",
                        null=True,
                    ),
                ),
                (
                    "vessel_performance",
                    models.TextField(
                        blank=True,
                        help_text="A description of the required handling characteristics of a vessel including hull design, main and auxilliary machinery, cargo handling equipment, navigation equipment and manoeuvring behaviour.",
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Applicabilities",
            },
        ),
        migrations.CreateModel(
            name="PilotageDistrict",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "communication_channel",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=list,
                        help_text="A channel number assigned to a specific radio frequency, frequencies or frequency band.<br/>ℹ️ Write comma separated values to define multiple.",
                        size=None,
                    ),
                ),
                ("geometry", s100.models.GMMultiSurface(srid=4326)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PilotBoardingPlace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "call_sign",
                    models.CharField(
                        blank=True,
                        help_text="The designated call-sign of a radio station.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category_of_pilot_boarding_place",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "boarding by pilot-cruising vessel",
                                "Boarding By Pilot Cruising Vessel",
                            ),
                            ("boarding by helicopter", "Boarding By Helicopter"),
                            (
                                "pilot comes out from shore",
                                "Pilot Comes Out From Shore",
                            ),
                        ],
                        help_text="Classification of pilot boarding place by method used to board pilots.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category_of_preference",
                    models.CharField(
                        blank=True,
                        choices=[("primary", "Primary"), ("alternate", "Alternate")],
                        help_text="The selection of one location compared to others.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category_of_vessel",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("general cargo vessel", "General Cargo Vessel"),
                            ("container carrier", "Container Carrier"),
                            ("tanker", "Tanker"),
                            ("bulk carrier", "Bulk Carrier"),
                            ("passenger vessel", "Passenger Vessel"),
                            ("roll-on roll-off", "Roll On Roll Off"),
                            ("refrigerated cargo vessel", "Refrigerated Cargo Vessel"),
                            ("fishing vessel", "Fishing Vessel"),
                            ("service", "Service"),
                            ("warship", "Warship"),
                            (
                                "towed or pushed composite unit",
                                "Towed Or Pushed Composite Unit",
                            ),
                            ("tug and tow", "Tug And Tow"),
                            ("light recreational", "Light Recreational"),
                            (
                                "semi-submersible offshore installation",
                                "Semi Submersible Offshore Installation",
                            ),
                            (
                                "jackup exploration or project installation",
                                "Jackup Exploration Or Project Installation",
                            ),
                            ("livestock carrier", "Livestock Carrier"),
                            ("sport fishing", "Sport Fishing"),
                        ],
                        help_text="Classification of vessels by function or use",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "communication_channel",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=list,
                        help_text="A channel number assigned to a specific radio frequency, frequencies or frequency band.<br/>ℹ️ Write comma separated values to define multiple.",
                        size=None,
                    ),
                ),
                (
                    "destination",
                    models.CharField(
                        blank=True,
                        help_text="The place or general direction to which a vessel is going or directed. Remarks: In addition to a placename of a port, harbour area or terminal, the place could include generalities such as “The north-west”, or “upriver”.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "pilot_movement",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("embarkation", "Embarkation"),
                            ("disembarkation", "Disembarkation"),
                            ("pilot change", "Pilot Change"),
                        ],
                        help_text="Classification of pilot activity by arrival, departure, or change of pilot. It may also describe the place where the pilot's advice begins, ends, or is transferred to a different pilot.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "pilot_vessel",
                    models.CharField(
                        blank=True,
                        help_text="Description of the pilot vessel. The pilot vessel is a small vessel used by a pilot to go to or from a vessel employing the pilot's services.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "status",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("permanent", "Permanent"),
                                ("occasional", "Occasional"),
                                ("recommended", "Recommended"),
                                ("not in use", "Not In Use"),
                                ("periodic/intermittent", "Periodic Intermittent"),
                                ("reserved", "Reserved"),
                                ("temporary", "Temporary"),
                                ("private", "Private"),
                                ("mandatory", "Mandatory"),
                                ("extinguished", "Extinguished"),
                                ("illuminated", "Illuminated"),
                                ("historic", "Historic"),
                                ("public", "Public"),
                                ("synchronised", "Synchronised"),
                                ("watched", "Watched"),
                                ("un-watched", "Un Watched"),
                                ("existence doubtful", "Existence Doubtful"),
                                ("buoyed", "Buoyed"),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.GeometryCollectionField(
                        srid=4326,
                        validators=[
                            s127.models.organisation_contact_area.validate_point_or_surface
                        ],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VesselsMeasurements",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vessels_characteristics",
                    models.CharField(
                        choices=[
                            ("length overall", "Length Overall"),
                            ("length at waterline", "Length At Waterline"),
                            ("breadth", "Breadth"),
                            ("draught", "Draught"),
                            ("height", "Height"),
                            ("displacement tonnage", "Displacement Tonnage"),
                            (
                                "displacement tonnage, light",
                                "Displacement Tonnage Light",
                            ),
                            (
                                "displacement tonnage, loaded",
                                "Displacement Tonnage Loaded",
                            ),
                            ("deadweight tonnage", "Deadweight Tonnage"),
                            ("gross tonnage", "Gross Tonnage"),
                            ("net tonnage", "Net Tonnage"),
                            (
                                "Panama Canal/Universal Measurement System net tonnage",
                                "Panama Canal Universal Measurement System Net Tonnage",
                            ),
                            ("Suez Canal net tonnage", "Suez Canal Net Tonnage"),
                            ("Suez Canal gross tonnage", "Suez Canal Gross Tonnage"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "comparison_operator",
                    models.CharField(
                        choices=[
                            ("greater than", "Greater Than"),
                            ("greater than or equal to", "Greater Than Or Equal To"),
                            ("less than", "Less Than"),
                            ("less than or equal to", "Less Than Or Equal To"),
                            ("equal to", "Equal To"),
                            ("not equal to", "Not Equal To"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "vessels_characteristics_value",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "vessels_characteristics_unit",
                    models.CharField(
                        choices=[
                            ("metre", "Metre"),
                            ("foot", "Foot"),
                            ("metric ton", "Metric Ton"),
                            ("ton", "Ton"),
                            ("short ton", "Short Ton"),
                            ("gross ton", "Gross Ton"),
                            ("net ton", "Net Ton"),
                            (
                                "Panama Canal/Universal Measurement System net tonnage",
                                "Panama Canal Universal Measurement System Net Tonnage",
                            ),
                            ("Suez Canal Net Tonnage", "Suez Canal Net Tonnage"),
                            ("none", "None"),
                            ("cubic metres", "Cubic Metres"),
                            ("Suez Canal Gross Tonnage", "Suez Canal Gross Tonnage"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "applicability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vessels_measurements",
                        to="s127.applicability",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PilotService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_of_pilot",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("pilot", "Pilot"),
                                ("deep sea", "Deep Sea"),
                                ("harbour", "Harbour"),
                                ("bar", "Bar"),
                                ("river", "River"),
                                ("channel", "Channel"),
                                ("lake", "Lake"),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Classification of pilots and pilot services by type of waterway where piloting services are provided.",
                        size=None,
                    ),
                ),
                (
                    "pilot_qualification",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("government pilot", "Government Pilot"),
                            (
                                "pilot approved by government",
                                "Pilot Approved By Government",
                            ),
                            ("state pilot", "State Pilot"),
                            ("federal pilot", "Federal Pilot"),
                            ("company pilot", "Company Pilot"),
                            ("local pilot", "Local Pilot"),
                            (
                                "citizen with sufficient local knowledge",
                                "Citizen With Sufficient Local Knowledge",
                            ),
                            (
                                "citizen with doubtful local knowledge",
                                "Citizen With Doubtful Local Knowledge",
                            ),
                        ],
                        help_text="Classification of pilots and pilot services by type of license qualification or type of organization providing services.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "pilot_request",
                    models.TextField(
                        blank=True,
                        help_text="Description of the pilot request procedure",
                        null=True,
                    ),
                ),
                (
                    "remote_pilot",
                    models.BooleanField(
                        choices=[(True, "Yes"), (False, "No")],
                        default=False,
                        help_text="Whether remote pilot services are available. True: remote pilot is available: Pilotage is available remotely from shore or other location remote from the vessel requiring pilotage.False: remote pilot is not available: Remote pilotage is not available.",
                    ),
                ),
                ("geometry", s100.models.GMMultiSurface(srid=4326)),
                (
                    "pilotage_district",
                    models.ForeignKey(
                        blank=True,
                        help_text="An area within which a pilotage direction exists.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pilot_services",
                        to="s127.pilotagedistrict",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PermissionType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_of_relationship",
                    models.CharField(
                        choices=[
                            ("prohibited", "Prohibited"),
                            ("not recommended", "Not Recommended"),
                            ("permitted", "Permitted"),
                            ("recommended", "Recommended"),
                            ("required", "Required"),
                            ("not required", "Not Required"),
                        ],
                        help_text="This attribute expresses the level of insistence for or against an action or activity.",
                        max_length=255,
                    ),
                ),
                ("feature_object_id", models.BigIntegerField()),
                (
                    "applicability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="s127.applicability",
                    ),
                ),
                (
                    "feature_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NoticeTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notice_time_hours",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.DurationField(),
                        blank=True,
                        default=list,
                        help_text="The time duration prior to the time the service is needed, when notice must be provided to the service provider.",
                        size=None,
                    ),
                ),
                (
                    "notice_time_text",
                    models.TextField(
                        blank=True,
                        help_text="Text string qualifying the notice time specified in NTCHRS.This may explain the time specification in NTCHRS (e.g., “3 working days” for a NTCHRS value of “72” where NTCTIM is supposed to be “3 working days”) or consist of other language qualifying the time, e.g., “On departure from last port” or “On passing reporting line XY”)",
                        null=True,
                    ),
                ),
                (
                    "operation",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("largest value", "Largest Value"),
                            ("smallest value", "Smallest Value"),
                        ],
                        help_text="Indicates whether the minimum or maximum value should be used to describe a condition or in application processing",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "pilot_service",
                    models.OneToOneField(
                        help_text="The service provided by a person who directs the movements of a vessel through pilot waters",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notice_time",
                        to="s127.pilotservice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
