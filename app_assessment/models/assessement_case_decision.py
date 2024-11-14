from base_module.model_fields import UUIDAutoField
from django.db import models

from app.models import ApplicationBaseModel, ApplicationDecisionType

from .assessment_update_mixin import AssessmentUpdateMixin
from .choices import DECISION_TYPE


class AssessmentCaseDecision(ApplicationBaseModel, AssessmentUpdateMixin):

    parent_object_id = UUIDAutoField(
        blank=True,
        editable=False,
        help_text="Parent ID primary key.",
        null=True,
    )

    parent_object_type = models.CharField(max_length=200, null=True, blank=True)

    author = models.CharField(max_length=200, null=True, blank=True)

    author_role = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    decision = models.CharField(
        max_length=200, choices=DECISION_TYPE, null=True, blank=True
    )

    status = models.ForeignKey(
        ApplicationDecisionType, on_delete=models.SET_NULL, null=True
    )

    date_approved = models.DateTimeField(null=True, blank=True)

    approved_by = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()

    class Meta:
        db_table = "assessment_case_decisions"
        verbose_name = "Assessment Case Decision"
        verbose_name_plural = "Assessment Case Decision"
