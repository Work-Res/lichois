from django.db import models

from app.models import ApplicationBaseModel

from .application_decision_type import ApplicationDecisionType


class ApplicationDecision(ApplicationBaseModel):

    final_decision_type = models.ForeignKey(
        ApplicationDecisionType,
        on_delete=models.CASCADE,
        related_name="final_decision_type",
        null=True,
        blank=True,
    )

    proposed_decision_type = models.ForeignKey(
        ApplicationDecisionType,
        on_delete=models.CASCADE,
        related_name="proposed_decision_type",
        null=True,
        blank=True,
    )

    comment = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Application Decision"
        ordering = ["-created"]
