from django.db import models

from app.classes.mixins.update_application_mixin import UpdateApplicationMixin
from app.models.application_base_model import ApplicationBaseModel


class DependantAssessment(ApplicationBaseModel, UpdateApplicationMixin):
    observation = models.TextField()
    recommendation = models.TextField()
    name_of_dependent = models.CharField(max_length=255)
    dependent_dob = models.DateField()
    reason_for_application = models.TextField()
    name_of_supporter = models.CharField(max_length=255)
    residential_status_of_supporter = models.CharField(max_length=255)
    relationship_to_applicant = models.CharField(max_length=255)
    nationality_of_dependent = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
