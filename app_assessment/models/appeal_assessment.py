from django.db import models

from app.models import ApplicationBaseModel


class AppealAssessment(ApplicationBaseModel):

    summary = models.TextField()

    recommendation = models.TextField()

    class Meta:

        verbose_name = "Appeal Assessment"
        verbose_name_plural = "Appeal Assessment"

    def __str__(self):
        return "Appeal Assessment"
