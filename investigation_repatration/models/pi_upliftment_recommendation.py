from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import ProhibitedImmigrant

class PIUpliftmentRecommendation(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='upliftment_recommendations')
    recommendation_reason = models.CharField(max_length=255)
    recommended_until = models.DateField(null=True, blank=True)
    recommended_by = models.CharField(max_length=255)
    recommendation_date = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(null=True, blank=True)