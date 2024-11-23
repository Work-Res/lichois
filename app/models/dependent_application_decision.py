from django.db import models

from app.models import ApplicationBaseModel, ApplicationDecision

from .application_decision_type import ApplicationDecisionType


class DependentApplicationDecision(ApplicationBaseModel):
    parent_object_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Parent ID primary key.",
    )

    parent_object_type = models.CharField(max_length=200, null=True, blank=True)

    principal_decision_type = models.ForeignKey(
        ApplicationDecision,
        on_delete=models.CASCADE,
        related_name="dependent_principal_decisions",  # Updated related_name
        null=True,
        blank=True,
    )

    dependent_decision = models.ForeignKey(
        ApplicationDecisionType,
        on_delete=models.CASCADE,
        related_name="dependent_application_decisions",  # Updated related_name
        null=True,
        blank=True,
    )

    comment = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Dependent Application Decisions"
        ordering = ["-created"]
