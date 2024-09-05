from django.db import models

from base_module.model_mixins import BaseUuidModel

from app_decision.models import ApplicationDecisionType


class CitizenshipMinisterDecision(BaseUuidModel):

    document_number = models.CharField(max_length=100, null=True, blank=True)

    date_requested = models.DateTimeField(auto_now_add=True)

    date_approved = models.DateTimeField(null=True, blank=True)

    status = models.ForeignKey(
        ApplicationDecisionType,
        on_delete=models.SET_NULL,
        null=True,
    )

    approved_by = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Citizenship Minister Decision"
