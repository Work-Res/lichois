from django.db import models

from app.models import ApplicationBaseModel
from .assessment_update_mixin import AssessmentUpdateMixin


class AppealAssessment(ApplicationBaseModel, AssessmentUpdateMixin):

    summary = models.TextField()

    recommendation = models.TextField()

    class Meta:

        verbose_name = "Appeal Assessment"
        verbose_name_plural = "Appeal Assessment"

    def __str__(self):
        return "Appeal Assessment"
