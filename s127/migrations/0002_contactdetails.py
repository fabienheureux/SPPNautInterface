# Generated by Django 4.1.7 on 2023-05-10 14:40

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import s127.models.shared


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("s127", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactDetails",
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
                    "call_name",
                    models.CharField(
                        blank=True,
                        help_text="The designated call name of a station, e.g. radio station, radar station, pilot. Remarks: This is the name used when calling a radio station by radio i.e. 'Singapore Pilots'.",
                        max_length=255,
                        null=True,
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
                    "category_of_comm_pref",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("preferred calling", "Preferred Calling"),
                            ("alternate calling", "Alternate Calling"),
                            ("preferred working", "Preferred Working"),
                            ("alternate working", "Alternate Working"),
                        ],
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
                    "contact_instructions",
                    models.TextField(
                        blank=True,
                        help_text="Supplemental instructions on how or when to contact the individual, organisation, or service",
                        null=True,
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[("fra", "French"), ("eng", "English")], max_length=3
                    ),
                ),
                (
                    "mmsi_code",
                    models.CharField(
                        blank=True,
                        help_text="The Maritime Mobile Service Identity (MMSI) Code is formed of a series of nine digits which are transmitted over the radio path in order to uniquely identify ship stations, ship earth stations, coast stations, coast earth stations, and group calls. These identities are formed in such a way that the identity or part thereof can be used by telephone and telex subscribers connected to the general telecommunications network principally to call ships automatically.",
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TimeIntervalsByDayOfWeek",
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
                ("object_id", models.BigIntegerField()),
                (
                    "day_of_week",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("Monday", "Monday"),
                                ("Tuesday", "Tuesday"),
                                ("Wednesday", "Wednesday"),
                                ("Thursday", "Thursday"),
                                ("Friday", "Friday"),
                                ("Saturday", "Saturday"),
                                ("Sunday", "Sunday"),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Encodes either range(s) of days or discrete days.",
                        size=None,
                    ),
                ),
                (
                    "day_of_week_is_range",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Yes"), (False, "No")],
                        help_text="Indicates whether the values in dayOfWeek indicate a range of days (true) or discrete days (false).",
                        null=True,
                    ),
                ),
                (
                    "time_of_day_start",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.DateTimeField(),
                        blank=True,
                        default=list,
                        help_text="Starting time of day, possibly for a period within the day. Distinction: Time start (TIMSTA) (S-101) which has a format YYYYMMDDThhmmss (mandatory) in the baseline S-101 DCEG as of October 2015.",
                        size=None,
                    ),
                ),
                (
                    "time_of_day_end",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.DateTimeField(),
                        blank=True,
                        default=list,
                        help_text="Ending time of day, possibly for a period within the day. Distinction: Time end (TIMEND) (S-101) which has a format YYYYMMDDThhmmss (mandatory) in the baseline S-101 DCEG as of October 2015.",
                        size=None,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Telecommunications",
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
                    "category_of_comm_pref",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("preferred calling", "Preferred Calling"),
                            ("alternate calling", "Alternate Calling"),
                            ("preferred working", "Preferred Working"),
                            ("alternate working", "Alternate Working"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "contact_instructions",
                    models.TextField(
                        blank=True,
                        help_text="Instructions on how and when to contact an individual or organisation",
                        null=True,
                    ),
                ),
                (
                    "telcom_carrier",
                    models.CharField(
                        blank=True,
                        help_text="The name of provider or type of carrier for a telecommunications service",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "telecommunication_identifier",
                    models.CharField(
                        help_text="Identifier used for contact by means of a telecommunications service, such as a telephone number",
                        max_length=255,
                    ),
                ),
                (
                    "telecommunication_service",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("voice", "Voice"),
                            ("facsimile", "Facsimile"),
                            ("sms", "Sms"),
                            ("data", "Data"),
                            ("streamedData", "Streamed Data"),
                            ("telex", "Telex"),
                            ("telegraph", "Telegraph"),
                            ("email", "Email"),
                        ],
                        help_text="Type of telecommunications service",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "contact_details",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="telecommunications",
                        to="s127.contactdetails",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ScheduleByDayOfWeek",
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
                    "category_of_schedule",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("normal operation", "Normal Operation"),
                            ("closure", "Closure"),
                            ("unmanned operation", "Unmanned Operation"),
                        ],
                        help_text="Describes the type of schedule, e.g., opening, closure, etc.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "telecommunications",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedulesbydayofweek",
                        to="s127.telecommunications",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Radiocommunications",
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
                    "category_of_comm_pref",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("preferred calling", "Preferred Calling"),
                            ("alternate calling", "Alternate Calling"),
                            ("preferred working", "Preferred Working"),
                            ("alternate working", "Alternate Working"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category_of_maritime_broadcast",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("navigational warning", "Navigational Warning"),
                                ("meteorological warning", "Meteorological Warning"),
                                ("ice report", "Ice Report"),
                                ("SAR information", "Sar Information"),
                                ("pirate attack warning", "Pirate Attack Warning"),
                                ("meteorological forecast", "Meteorological Forecast"),
                                ("pilot service message", "Pilot Service Message"),
                                ("AIS information", "Ais Information"),
                                ("LORAN message", "Loran Message"),
                                ("SATNAV message", "Satnav Message"),
                                ("gale warning", "Gale Warning"),
                                ("storm warning", "Storm Warning"),
                                (
                                    "tropical revolving storm warning",
                                    "Tropical Revolving Storm Warning",
                                ),
                                ("NAVAREA warning", "Navarea Warning"),
                                ("coastal warning", "Coastal Warning"),
                                ("local warning", "Local Warning"),
                                (
                                    "low water level warning/negative tidal surge",
                                    "Low Water Level Warning Negative Tidal Surge",
                                ),
                                ("icing warning", "Icing Warning"),
                                ("tsunami broadcast", "Tsunami Broadcast"),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Classification of maritime broadcast based on the nature of information conveyed.",
                        size=None,
                    ),
                ),
                (
                    "category_of_radio_methods",
                    s127.models.shared.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                (
                                    "Low Frequency (LF) voice traffic",
                                    "Low Frequency Lf Voice Traffic",
                                ),
                                (
                                    "Medium Frequency (MF) voice traffic",
                                    "Medium Frequency Mf Voice Traffic",
                                ),
                                (
                                    "High Frequency (HF) voice traffic",
                                    "High Frequency Hf Voice Traffic",
                                ),
                                (
                                    "Very High Frequency (VHF) voice traffic",
                                    "Very High Frequency Vhf Voice Traffic",
                                ),
                                (
                                    "High Frequency Narrow Band Direct Printing",
                                    "High Frequency Narrow Band Direct Printing",
                                ),
                                ("NAVTEX", "Navtex"),
                                ("SafetyNET", "Safety Net"),
                                (
                                    "NBDP Telegraphy (Narrow Band Direct Printing Telegraphy)",
                                    "Nbdp Telegraphy Narrow Band Direct Printing Telegraphy",
                                ),
                                ("facsimile", "Facsimile"),
                                ("NAVIP", "Navip"),
                                (
                                    "Low Frequency (LF) digital traffic",
                                    "Low Frequency Lf Digital Traffic",
                                ),
                                (
                                    "Medium Frequency (MF) digital traffic",
                                    "Medium Frequency Mf Digital Traffic",
                                ),
                                (
                                    "High Frequency (HF) digital traffic",
                                    "High Frequency Hf Digital Traffic",
                                ),
                                (
                                    "Very High Frequency (VHF) digital traffic",
                                    "Very High Frequency Vhf Digital Traffic",
                                ),
                                (
                                    "Low Frequency (LF) telegraph traffic",
                                    "Low Frequency Lf Telegraph Traffic",
                                ),
                                (
                                    "Medium Frequency (MF) telegraph traffic",
                                    "Medium Frequency Mf Telegraph Traffic",
                                ),
                                (
                                    "High Frequency (HF) telegraph traffic",
                                    "High Frequency Hf Telegraph Traffic",
                                ),
                                (
                                    "Medium Frequency (MF) Digital Selective Call traffic",
                                    "Medium Frequency Mf Digital Selective Call Traffic",
                                ),
                                (
                                    "High Frequency (HF) Digital Selective Call traffic",
                                    "High Frequency Hf Digital Selective Call Traffic",
                                ),
                                (
                                    "Very High Frequency (VHF) Digital Selective Call traffic",
                                    "Very High Frequency Vhf Digital Selective Call Traffic",
                                ),
                            ],
                            max_length=255,
                        ),
                        blank=True,
                        default=list,
                        help_text="Categories of radiocommunications based on frequency band and radio traffic method.",
                        size=None,
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
                    "contact_instructions",
                    models.TextField(
                        blank=True,
                        help_text="Supplemental instructions on how or when to contact the individual, organisation, or service",
                        null=True,
                    ),
                ),
                (
                    "signal_frequency",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "transmission_content",
                    models.CharField(
                        blank=True,
                        help_text="Content of transmission. Remarks: Not to be used if CATMAB is populated",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "contact_details",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="radiocommunications",
                        to="s127.contactdetails",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OnlineResource",
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
                    "linkage",
                    models.URLField(
                        help_text="Location (address) for on-line access using a URL/URI address or similar addressing scheme. (Adapted from ISO 19115:2014.)"
                    ),
                ),
                (
                    "protocol",
                    models.CharField(
                        blank=True,
                        help_text="Connection protocol to be used. Example: ftp, http get KVP, http POST, etc. (ISO 19115)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "application_profile",
                    models.CharField(
                        blank=True,
                        help_text="Name of an application profile that can be used with the online resource (ISO 19115)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "name_of_resource",
                    models.CharField(
                        blank=True,
                        help_text="Name of the online resource (ISO 19115, adapted)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "online_resource_description",
                    models.CharField(
                        blank=True,
                        help_text="Detailed text description of what the online resource is/does (ISO 19115)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "online_function",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("download", "Download"),
                            ("information", "Information"),
                            ("offline access", "Offline Access"),
                            ("order", "Order"),
                            ("search", "Search"),
                            ("complete metadata", "Complete Metadata"),
                            ("browse graphic", "Browse Graphic"),
                            ("upload", "Upload"),
                            ("email service", "Email Service"),
                            ("browsing", "Browsing"),
                            ("file access", "File Access"),
                        ],
                        help_text="Code for function performed by the online resource (ISO 19115)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "protocol_request",
                    models.CharField(
                        blank=True,
                        help_text="Request used to access the resource. Structure and content depend on the protocol and standard used by the online resource, such as Web Feature Service standard. (ISO 19115, adapted)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "contact_details",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="online_resources",
                        to="s127.contactdetails",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FrequencyPair",
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
                ("object_id", models.BigIntegerField()),
                (
                    "frequency_shore_station_transmits",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(),
                        blank=True,
                        default=list,
                        help_text="The shore station transmitter frequency expressed in kHz to one decimal place. Units: kHZ, Resolution: 0.1, Format: XXXXXX Examples: 4379.1 kHz becomes 043791; 13162.8 kHz becomes 131628",
                        size=None,
                    ),
                ),
                (
                    "frequency_shore_station_receives",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(),
                        blank=True,
                        default=list,
                        help_text="The shore station receiver frequency expressed in kHz to one decimal place. Units: kHz, Resolution: 0.1, Format: XXXXXX Examples: 4379.1 kHz becomes 043791; 13162.8 kHz becomes 131628",
                        size=None,
                    ),
                ),
                (
                    "contact_instructions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.TextField(),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContactAddress",
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
                    "delivery_point",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=list,
                        help_text="Details of where post can be delivered such as the apartment, name and/or number of a street, building or PO Box.",
                        size=None,
                    ),
                ),
                (
                    "city_name",
                    models.CharField(
                        blank=True,
                        help_text="The name of a town or city.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "administrative_division",
                    models.CharField(
                        blank=True,
                        help_text="Administrative division is a generic term for an administrative region within a country at a level below that of the sovereign state.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "country_name",
                    models.CharField(
                        blank=True,
                        help_text="The name of a nation. (Adapted from The American Heritage Dictionaries)",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True,
                        help_text="Known in various countries as a postcode, or ZIP code, the postal code is a series of letters and/or digits that identifies each postal delivery area.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "contact_details",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact_addresses",
                        to="s127.contactdetails",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
