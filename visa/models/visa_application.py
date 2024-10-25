from django.db import models

from app.models.application_base_model import ApplicationBaseModel
from app_personal_details.models.passport import Passport
from visa.models import VisaReference, CurrencyAmount

from ..choices import ENTRY_FREQ, VISA_TYPES
from django.utils.translation import gettext_lazy as _

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

    currency_amounts = models.ManyToManyField(
        CurrencyAmount,
        related_name='currency_amounts',
        blank=True,null=True
    )

    currency_code_other = models.CharField(
        verbose_name = _("If OTHER currency, specify ..."),
        blank=True,null=True
    )

    passport = models.ForeignKey(
        Passport,
        on_delete=models.CASCADE,
        related_name="applicant_passport",
        null=True,
    )

    amount_other = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

    return_visa_to = models.CharField(max_length=200, blank=True, null=True)

    valid_until = models.DateField()

    class Meta:
        app_label = "visa"
