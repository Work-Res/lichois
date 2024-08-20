from django.db import models
from app.models import ApplicationBaseModel


class ExemptionCertificate(ApplicationBaseModel):

    business_name = models.CharField(max_length=150)
    employment_capacity = models.CharField(max_length=250)
    proposed_period = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Exemption Certificate"
