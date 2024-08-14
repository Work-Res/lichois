from django.db import models

from app.models import ApplicationBaseModel

from .parent_manager import ParentModelManager


class AssessmentCaseSummary(ApplicationBaseModel):

    parent_object_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Parent ID primary key.",
    )

    parent_object_type = models.CharField(max_length=200, null=True, blank=True)

    summary = models.TextField(max_length=4000)

    data = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        db_table = "assessment_case_summary"
        verbose_name = "Assessment Case Summary"
        verbose_name_plural = "Assessment Case Summary"

    def parent_object(self):
        app_label, model_name = self.parent_object_type.split(".")
        parents = ParentModelManager(app_label=app_label, model_name=model_name)
        return parents.get_model().objects.get(id=self.parent_object_id)
