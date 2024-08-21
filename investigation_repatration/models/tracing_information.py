from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import ProhibitedImmigrant
    
class PresidentialDeclaration(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='declarations')
    declaration_date = models.DateField()
    declaration_reason = models.TextField()
    declared_by = models.CharField(max_length=255)  
    declared_status = models.CharField(max_length=50, choices=[('Prohibited', 'Prohibited'), ('Under Investigation', 'Under Investigation')], default='Prohibited')
    official_document = models.FileField(upload_to='declarations/')  
    
    
class MovementLog(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='movements')
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    reason_for_presence = models.TextField(null=True, blank=True)
    observed_by = models.CharField(max_length=255)  
    
    
class Interaction(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    involved_personnel = models.CharField(max_length=255)  