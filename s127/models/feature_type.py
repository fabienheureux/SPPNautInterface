from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

import s100.models


class PilotageDistrict(s100.models.FeatureType):
    communication_channel = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
        help_text="A channel number assigned to a specific radio frequency, frequencies or frequency band.<br/>"
        "ℹ️ Write comma separated values to define multiple.",
    )

    # Spec says it is optional. We've decided to make it mandatory.
    geometry = s100.models.GMMultiSurface()

    # Uncomment when upgrading to django 4.2
    # class Meta:
    #     db_table_comment = "An area within which a pilotage direction exists. "
    #     "Such directions are regulated by a competent harbour authority which "
    #     "dictates circumstances under which they apply."


class SimplePilotageDistrictProxy(PilotageDistrict):
    class Meta:
        proxy = True
        verbose_name = "Pilotage district (simple form)"
        verbose_name_plural = "Pilotages district (simple form)"


class FullPilotageDistrictProxy(PilotageDistrict):
    class Meta:
        proxy = True
        verbose_name = "Pilotage district (full form)"
        verbose_name_plural = "Pilotages district (full form)"
