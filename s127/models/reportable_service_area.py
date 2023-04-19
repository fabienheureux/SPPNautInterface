from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

import s100.models
from s127.models.feature_type import PilotageDistrict

from .shared import BooleanChoices, ChoiceArrayField, S127ReportableServiceArea


class S127PilotService(S127ReportableServiceArea):
    class CategoryOfPilot(models.TextChoices):
        """
        Classification of pilots and pilot services by type of waterway where
        piloting services are provided.

        :cvar PILOT: Pilot licenced to conduct vessels during approach from
            sea to a specified place which may be a handover place, an
            anchorage or alongside.
        :cvar DEEP_SEA: Pilot licenced to conduct vessels over extensive sea
            areas.
        :cvar HARBOUR: Pilot who is licenced to conduct vessels from a
            specified place, such as a handover area or anchorage into a
            harbour.
        :cvar BAR: Pilot licensed to conduct vessels over a bar to or from a
            handover with a river pilot (for example as used in USA).
        :cvar RIVER: Pilot licensed to conduct vessels from and to specified
            places, along the course of a river (for example as used in Rio
            Amazonas and Rio de La Plata).
        :cvar CHANNEL: Pilot licensed to conduct vessels from and to
            specified places, along the course of a channel. (for example as
            used in Rio Amazonas and Rio de La Plata).
        :cvar LAKE: Pilot licensed to conduct vessels from and to specified
            places on a great lake. (for example as used in the Lago de
            Maracaibo in Venezuela.
        """

        PILOT = "pilot"
        DEEP_SEA = "deep sea"
        HARBOUR = "harbour"
        BAR = "bar"
        RIVER = "river"
        CHANNEL = "channel"
        LAKE = "lake"

    class PilotQualification(models.TextChoices):
        """
        Classification of pilots and pilot services by type of license
        qualification or type of organization providing services.

        :cvar GOVERNMENT_PILOT: A pilot service carried out by government
            pilots.
        :cvar PILOT_APPROVED_BY_GOVERNMENT: A pilot service carried out by
            pilots who are approved by government.
        :cvar STATE_PILOT: A pilot that is licensed by the State (USA)
            and/or their respective pilot association, required for all
            foreign vessels and all American vessels under registry, bound
            for a port with compulsory State pilotage. A federal licence is
            not sufficient to pilot such vessels into the port.
        :cvar FEDERAL_PILOT: A pilot who carries a Federal endorsement,
            offering services to vessels that are not required to obtain
            compulsory State pilotage. Services are usually contracted for
            in advance.
        :cvar COMPANY_PILOT: A pilot provided by a commercial company.
        :cvar LOCAL_PILOT: A pilot with local knowledge but who does not
            hold a qualification as a pilot.
        :cvar CITIZEN_WITH_SUFFICIENT_LOCAL_KNOWLEDGE: A pilot service
            carried out by a citizen with sufficient local knowledge.
        :cvar CITIZEN_WITH_DOUBTFUL_LOCAL_KNOWLEDGE: A pilot service carried
            out by a citizen whose local knowledge is uncertain.
        """

        GOVERNMENT_PILOT = "government pilot"
        PILOT_APPROVED_BY_GOVERNMENT = "pilot approved by government"
        STATE_PILOT = "state pilot"
        FEDERAL_PILOT = "federal pilot"
        COMPANY_PILOT = "company pilot"
        LOCAL_PILOT = "local pilot"
        CITIZEN_WITH_SUFFICIENT_LOCAL_KNOWLEDGE = (
            "citizen with sufficient local knowledge"
        )
        CITIZEN_WITH_DOUBTFUL_LOCAL_KNOWLEDGE = "citizen with doubtful local knowledge"

    pilotage_district = models.ForeignKey(
        PilotageDistrict,
        on_delete=models.CASCADE,
        related_name="pilot_service",
        blank=True,
        null=True,
    )
    category_of_pilot = ChoiceArrayField(
        base_field=models.CharField(
            max_length=255,
            choices=CategoryOfPilot.choices,
        ),
        default=list,
        blank=True,
        null=True,
    )
    pilot_qualification = models.CharField(
        max_length=255,
        choices=PilotQualification.choices,
        blank=True,
        null=True,
        help_text="",
    )
    pilot_request = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Description of the pilot request procedure",
    )
    remote_pilot = models.BooleanField(
        null=True,
        blank=True,
        choices=BooleanChoices.choices,
        help_text="Whether remote pilot services are available. "
        "True: remote pilot is available: Pilotage is available remotely from shore or other location remote from the vessel requiring pilotage."
        "False: remote pilot is not available: Remote pilotage is not available.",
    )
    # FIXME: GM_OrientableSurface ? 0..* ?
    geometry = models.MultiPolygonField()

    # Uncomment when upgrading to django 4.2
    # class Meta:
    #     db_table_comment = "The service provided by a person who directs the movements of a vessel through pilot waters, "
    #     "usually a person who has demonstrated extensive knowledge of channels, aids to navigation, dangers to navigation, etc., "
    #     "in a particular area and is licensed for that area."


class S127NoticeTime(s100.models.ComplexAttributeType):
    class Operation(models.TextChoices):
        """Indicates whether the minimum or maximum value should be used to describe a condition or in application processing
        Remarks: OPERAT is intended to be used in conjunction with other attributes (or sub-attributes of a complex attribute) to indicate how their values must be combined in order to describe a condition. Null attributes are ignored.
        Example: Complex attribute underkeelAllowance with UKCFIX=2.5, UKCVAR=10.00, OPERAT=1 inicates that the under-keel allowance required is the greater of 2.5 metres or 10% of the ship's draught.

        :cvar LARGEST_VALUE: The numerically largest value computed from the
            applicable attributes or sub-attributes
        :cvar SMALLEST_VALUE: The numerically smallest value computed from
            the applicable attributes or sub-attributes
        """

        LARGEST_VALUE = "largest value"
        SMALLEST_VALUE = "smallest value"

    pilot_service = models.ForeignKey(
        S127PilotService, on_delete=models.CASCADE, related_name="notice_time"
    )
    notice_time_hours = ArrayField(
        models.FloatField(),
        help_text="The time duration prior to the time the service is needed, when notice must be provided to the service provider.",
    )
    notice_time_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Text string qualifying the notice time specified in NTCHRS."
        "This may explain the time specification in NTCHRS (e.g., “3 working days” for a NTCHRS value of “72” where NTCTIM is supposed to be “3 working days”)"
        " or consist of other language qualifying the time, e.g., “On departure from last port” or “On passing reporting line XY”)",
    )
    operation = models.CharField(
        max_length=255,
        choices=Operation.choices,
        blank=True,
        null=True,
        help_text="Indicates whether the minimum or maximum value should be used to describe a condition or in application processing",
    )
