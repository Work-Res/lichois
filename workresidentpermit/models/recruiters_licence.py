from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import GENDER, YES_NO
from .resident_permit import ResidencePermit


class RecruitersLicence(BaseUuidModel):

    physical_address_id = models.CharField(max_length=150)
    postal_address_id = models.CharField(max_length=150)
    contact_details_id = models.CharField(max_length=150)

    license_type = models.CharField(max_length=150)
    employment_nature = models.CharField(max_length=150)
    date_signed = models.DateField()
    applicant_name = models.CharField(max_length=150)
    applicant_position = models.CharField(max_length=150)
    signature = models.CharField(max_length=150)

    class Meta:
        app_label = "workresidentpermit"
        verbose_name = "Child"
