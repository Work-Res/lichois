from django.db import models
from app.models import ApplicationBaseModel


class EmergencyPermit(ApplicationBaseModel):
    nature_emergency = models.CharField(max_length=255)
    job_requirements = models.CharField(max_length=255)
    services_provided = models.CharField(max_length=255)
    chief_authorization = models.CharField(max_length=255)
    capacity = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Emergency Permit"
