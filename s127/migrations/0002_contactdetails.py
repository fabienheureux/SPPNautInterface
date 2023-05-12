# Generated by Django 4.1.7 on 2023-05-12 10:24

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
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
                        blank=True,
                        choices=[("fra", "French"), ("eng", "English")],
                        max_length=3,
                        null=True,
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
                "verbose_name_plural": "Contact Details",
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
                    "postal_code",
                    models.CharField(
                        blank=True,
                        help_text="Known in various countries as a postcode, or ZIP code, the postal code is a series of letters and/or digits that identifies each postal delivery area.",
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
