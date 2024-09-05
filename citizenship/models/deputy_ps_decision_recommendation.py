from django.db import models

from app.models import ApplicationBaseModel
from citizenship.models.model_mixins import RecommendationUpdateMixin
from .roles_choices import DECISION_AUTHORITY_CHOICES


class CitizenshipRecommendation(ApplicationBaseModel, RecommendationUpdateMixin):

    role = models.CharField(
        choices=DECISION_AUTHORITY_CHOICES, max_length=50, null=True, blank=True
    )

    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()

    class Meta:

        db_table = "citizenship_recommendation"
        verbose_name = "Citizenship Recommendation"
        verbose_name_plural = "Citizenship Recommendation"

    def __str__(self):
        return f"Assessment Emergency: {self.document_number}, {self.comment}"
