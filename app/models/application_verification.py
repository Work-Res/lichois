from django.db import models
from .application_base_model import ApplicationBaseModel

from app_decision.models import ApplicationDecisionType


class ApplicationVerification(ApplicationBaseModel):

    decision = models.ForeignKey(
        ApplicationDecisionType, on_delete=models.SET_NULL, null=True
    )
    summary = models.TextField(null=True, blank=True)

    date_approved = models.DateTimeField(null=True, blank=True)

    approved_by = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.decision}"

    class Meta:
        app_label = "app"
