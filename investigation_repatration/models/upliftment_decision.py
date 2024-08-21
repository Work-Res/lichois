from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import ProhibitedImmigrant, PIExemption, PIUpliftmentRecommendation

choices=[
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
            ('Deferred', 'Deferred'),
            ('Revoked', 'Revoked')
        ]

class UpliftmentDecision(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='upliftment_decisions')
    exemption = models.ForeignKey(PIExemption, on_delete=models.SET_NULL, null=True, blank=True, related_name='upliftment_decisions')
    upliftment_recommendation = models.ForeignKey(PIUpliftmentRecommendation, on_delete=models.SET_NULL, null=True, blank=True, related_name='upliftment_decisions')
    decision = models.CharField(max_length=50,choices=choices,default='Deferred')
    decision_date = models.DateTimeField(auto_now_add=True)
    decided_by = models.CharField(max_length=255)
    decision_reason = models.TextField(null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
