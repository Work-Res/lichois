from django.db import models

from app.models.application_base_model import ApplicationBaseModel
from .assessment_update_mixin import AssessmentUpdateMixin


class DependantAssessment(ApplicationBaseModel, AssessmentUpdateMixin):
    observation = models.TextField()
    recommendation = models.TextField()
    name_of_dependent = models.CharField(max_length=255)
    dependent_dob = models.DateField(null=True, blank=True)
    reason_for_application = models.TextField()
    name_of_supporter = models.CharField(max_length=255)
    residential_status_of_supporter = models.CharField(max_length=255)
    relationship_to_applicant = models.CharField(max_length=255)
    nationality_of_dependent = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()
