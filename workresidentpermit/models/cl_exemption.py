from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import GENDER, YES_NO
from .resident_permit import ResidencePermit


class CommissionerLabourExemption(BaseUuidModel):

    emergency_nature = models.TextField(max_length=250)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    job_requirements = models.TextField(max_length=250)
    nationality = models.CharField(max_length=150)
    # passport_details_id

    employment_company = models.CharField(max_length=150)
    company_products_services = models.TextField(max_length=250)
    immigration_office_waiver = models.CharField(max_length=5)
    # TODO: waiver_attachment
    applicant_signature = models.CharField(max_length=150)
    applicant_capacity = models.CharField(max_length=150)
    application_date = models.DateField()
    decision = models.CharField(max_length=150)
    decision_reasons = models.TextField(max_length=300)
    authorising_officer = models.CharField(max_length=150)
    signature = models.CharField(max_length=150)

    # attachments

    class Meta:
        verbose_name = "Child"
