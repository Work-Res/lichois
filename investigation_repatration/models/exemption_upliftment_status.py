from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import ProhibitedImmigrant, PIUpliftmentRecommendation, PIExemption


choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
            ('Revoked', 'Revoked')
        ]

class ExemptionUpliftmentStatus(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='upliftment_statuses')
    upliftment_recommendation = models.ForeignKey(PIUpliftmentRecommendation, on_delete=models.SET_NULL, null=True, blank=True, related_name='upliftment_statuses')
    exemption = models.ForeignKey(PIExemption, on_delete=models.SET_NULL, null=True, blank=True, related_name='upliftment_statuses')
    status = models.CharField(max_length=50,choices=choices,default='Pending')
    status_date = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.CharField(max_length=255)
    additional_notes = models.TextField(null=True, blank=True)

