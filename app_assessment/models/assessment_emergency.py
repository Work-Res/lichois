from django.db import models

from app.models import ApplicationBaseModel
from .assessment_update_mixin import AssessmentUpdateMixin


class AssessmentEmergency(ApplicationBaseModel, AssessmentUpdateMixin):

    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()

    class Meta:

        db_table = "assessment_emergency"
        verbose_name = "Assessment Emergency"
        verbose_name_plural = "Assessment Emergency"

    def __str__(self):
        return f"Assessment Emergency: {self.competency}, {self.qualification}"
