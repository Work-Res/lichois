from django.db import models
from base_module.model_mixins import BaseUuidModel
from .recruiters_licence import RecruitersLicense


class WageRate(BaseUuidModel):

    recruiters_license = models.ForeignKey(RecruitersLicense, on_delete=models.CASCADE)
    class_position = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)

    class Meta:
        app_label = "workresidentpermit"
