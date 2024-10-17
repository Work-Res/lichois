from django.db import models

from app.models.application_base_model import ApplicationBaseModel
from visa.models.visa_reference import VisaReference

from ..choices import ENTRY_FREQ, VISA_TYPES


class VisaApplication(ApplicationBaseModel):
    visa_type = models.CharField(choices=VISA_TYPES, max_length=50)
    no_of_entries = models.CharField(choices=ENTRY_FREQ, max_length=10)
    nationality = models.CharField(max_length=100)

    proposed_durations_stay = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)

    travel_reasons = models.TextField(
        verbose_name="Reasons in full for wishing to travel to the Republic of Botswana",
    )

    # Requested Validity Period of Visa
    requested_valid_from = models.DateField()  # validators=[date_not_past]

    requested_valid_to = models.DateField()  # validators=[date_not_past]

    references = models.ManyToManyField(
        VisaReference,
        related_name="references",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "visa"
