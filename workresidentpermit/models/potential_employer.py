from django.db import models
from base_module.model_mixins import BaseUuidModel
from .recruiters_licence import RecruitersLicense


class PotentialEmployer(BaseUuidModel):

    recruiters_license = models.ForeignKey(RecruitersLicense, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)

    # physical_address
    # postal_address
    # contacts

    class Meta:
        app_label = "workresidentpermit"
