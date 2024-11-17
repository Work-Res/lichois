from django.db import models

from app.models.application_base_model import ApplicationBaseModel
from app.utils import ApplicationDecisionEnum
from app_personal_details.models import Spouse, Child


class DependantAssessment(ApplicationBaseModel):
    observation = models.TextField()
    recommendation = models.TextField()
    name_of_dependent = models.CharField(max_length=255)
    dependent_dob = models.DateField(null=True, blank=True)
    reason_for_application = models.TextField()
    name_of_supporter = models.CharField(max_length=255)
    residential_status_of_supporter = models.CharField(max_length=255)
    relationship_to_applicant = models.CharField(max_length=255)
    nationality_of_dependent = models.CharField(max_length=255)

    assessment = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    spouse = models.ForeignKey(
        Spouse,
        on_delete=models.CASCADE,  # Adjust on_delete behavior as needed
        related_name="dependant_assessments",  # Optional: Add related_name for reverse lookup
        null=True,  # Optional: Allow null values if a dependent is not always linked to a spouse
        blank=True,  # Optional: Allow blank values in forms
    )

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,  # Adjust on_delete behavior as needed
        related_name="dependant_assessments",  # Reverse lookup for child
        null=True,  # Allow null for optional relation
        blank=True,
    )

    class Meta:
        verbose_name = "Dependant Assessment"
        verbose_name_plural = "Dependant Assessments"
