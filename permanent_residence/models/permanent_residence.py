from django.db import models

from app.models.application_base_model import ApplicationBaseModel

from .previous_country_residence import PreviousCountryResidence


class PermanentResidence(ApplicationBaseModel):

    investor_contribution = models.CharField(max_length=255, blank=True, null=True)
    employee_contribution = models.CharField(max_length=255, blank=True, null=True)
    any_other_resident = models.CharField(max_length=255, blank=True, null=True)
    violated_terms_before = models.CharField(max_length=255, blank=True, null=True)
    preferred_method_comm = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    spouse_applying_residence = models.CharField(max_length=255, blank=True, null=True)
    prohibited_in_botswana = models.CharField(max_length=255, blank=True, null=True)
    reasons_prohibited = models.CharField(max_length=255, blank=True, null=True)
    imprisonment_any_country = models.CharField(max_length=255, blank=True, null=True)
    reasons_imprisonment = models.CharField(max_length=255, blank=True, null=True)
    permit_reasons = models.CharField(max_length=255, blank=True, null=True)
    period_when_required = models.DateField(blank=True, null=True)
    take_up_occupation = models.CharField(max_length=255, blank=True, null=True)
    application_reason = models.CharField(max_length=255, blank=True, null=True)
    application_reason_other = models.CharField(max_length=255, blank=True, null=True)
    application_status = models.CharField(max_length=255, blank=True, null=True)
    previous_country_residence = models.ManyToManyField(
        PreviousCountryResidence,
        blank=True,
        null=True,
    )
