from django.db import models

from app.models import ApplicationBaseModel
from ..choices import APPEAL_TYPE


class PermitAppeal(ApplicationBaseModel):
    reason_for_appeal = models.TextField()
    appeal_type = models.CharField(
        max_length=250,
        choices=APPEAL_TYPE,
        default="appeal",
    )
    appeal_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Work Residence Permit Appeal"
        verbose_name_plural = "Work Residence Permit Appeals"
