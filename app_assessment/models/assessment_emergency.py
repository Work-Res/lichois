from django.db import models

from app.models import ApplicationBaseModel


class AssessmentEmergency(ApplicationBaseModel):

    comment = models.TextField()

    class Meta:

        db_table = 'assessment_emergency'
        verbose_name = 'Assessment Emergency'
        verbose_name_plural = 'Assessment Emergency'

    def __str__(self):
        return f"Assessment Emergency: {self.competency}, {self.qualification}"
