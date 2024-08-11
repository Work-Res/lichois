from django.db import models

from app.models import ApplicationBaseModel


class SummaryAssessment(ApplicationBaseModel):
    summary = models.TextField(blank=True, null=True)
