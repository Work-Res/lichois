from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import GENDER, YES_NO
from .resident_permit import ResidencePermit


class RecruitersApplicationDecision(BaseUuidModel):

    recruiters_application_id = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    signature = models.CharField(max_length=250)
    decision_taken = models.CharField(max_length=250)
    decision_date = models.DateField(max_length=250)
    decision_sign = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Child"
