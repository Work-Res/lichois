from django.db import models
from app.models import ApplicationBaseModel

from ..choices import CERTIFICATE_STATUS


class PermitReplacement(ApplicationBaseModel):
    date_signed = models.DateField()
    signature = models.CharField(max_length=255)
    certificate_status = models.CharField(max_length=255, choices=CERTIFICATE_STATUS)
    date_issued = models.DateField()

    class Meta:
        verbose_name = "Replacement Permit"
