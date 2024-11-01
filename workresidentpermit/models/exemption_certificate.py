from django.db import models
from app.models import ApplicationBaseModel


class ExemptionCertificate(ApplicationBaseModel):

    business_name = models.CharField(max_length=150)
    employment_capacity = models.CharField(max_length=250)
    proposed_period = models.CharField(max_length=150)
    relevant_experience = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Exemption Certificate"
