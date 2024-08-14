from django.db import models

from app.models import ApplicationBaseModel

from .assessment_update_mixin import AssessmentUpdateMixin


class SummaryAssessment(ApplicationBaseModel, AssessmentUpdateMixin):
    summary = models.TextField()
