from django.db import models
from app.models.application_base_model import ApplicationBaseModel
from visa.models.visa_reference import VisaReference
from ..choices import ENTRY_FREQ, VISA_TYPES


class VisaApplication(ApplicationBaseModel):
    visa_type = models.CharField(
        choices=VISA_TYPES,
        max_length=50,
        verbose_name="Type of Visa",
        help_text="Select the type of visa being applied for.",
    )
    no_of_entries = models.CharField(
        choices=ENTRY_FREQ,
        max_length=10,
        verbose_name="Number of Entries",
        help_text="Indicate the number of entries you require for this visa.",
    )
    proposed_durations_stay = models.CharField(
        max_length=100,
        verbose_name="Proposed Duration of Stay",
        help_text="Specify how long you intend to stay in Botswana.",
    )
    travel_reasons = models.TextField(
        verbose_name="Reasons for Traveling to Botswana",
        help_text="Provide detailed reasons for traveling to the Republic of Botswana.",
    )
    # Requested Validity Period of Visa
    requested_valid_from = models.DateField(
        verbose_name="Requested Start Date",
        help_text="Specify the date from which the visa should be valid.",
    )
    requested_valid_to = models.DateField(
        verbose_name="Requested End Date",
        help_text="Specify the date until which the visa should be valid.",
    )
    references = models.ManyToManyField(
        VisaReference,
        related_name="visa_applications",
        blank=True,
        verbose_name="References",
        help_text="Add references for this visa application.",
    )

    class Meta:
        app_label = "visa"
        verbose_name = "Visa Application"
        verbose_name_plural = "Visa Applications"

