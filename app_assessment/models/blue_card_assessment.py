from django.db import models

from app.models import ApplicationBaseModel
from .assessment_update_mixin import AssessmentUpdateMixin


class BlueCardAssessment(ApplicationBaseModel, AssessmentUpdateMixin):
    name_of_supporter = models.CharField(max_length=255)
    relationship_to_supporter = models.CharField(max_length=255)
    observations = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()
