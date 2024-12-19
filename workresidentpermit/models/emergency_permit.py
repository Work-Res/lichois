from django.db import models
from app.models import ApplicationBaseModel
from ..choices import EMERGENCY_PERIOD


class EmergencyPermit(ApplicationBaseModel):
    nature_emergency = models.CharField(max_length=255,verbose_name='Nature of Emergency')
    job_requirements = models.CharField(max_length=255,verbose_name='Job Requirements')
    services_provided = models.CharField(max_length=255,verbose_name='What products/Services does the Company provide?')
    chief_authorization = models.CharField(max_length=255,verbose_name='Signature')
    capacity = models.CharField(max_length=255, verbose_name='Capacity')
    emergency_period = models.CharField(
        max_length=255,
        choices=EMERGENCY_PERIOD,
    )

    class Meta:
        verbose_name = "Emergency Permit"
