
from django.db import models

from app.models import ApplicationBaseModel
from citizenship.models.model_mixins import RecommendationUpdateMixin


class CitizenshipRecommendation(ApplicationBaseModel, RecommendationUpdateMixin):

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