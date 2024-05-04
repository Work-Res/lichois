from django.db import models

from app.models import ApplicationBaseModel


class AssessmentResult(ApplicationBaseModel):

    score = models.IntegerField()
    output_results = models.JSONField()
    result_date = models.DateField()

    def __str__(self):
        return self.title
