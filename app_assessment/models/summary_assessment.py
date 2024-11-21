from django.db import models

from app.models import ApplicationBaseModel


class SummaryAssessment(ApplicationBaseModel):
    summary = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
