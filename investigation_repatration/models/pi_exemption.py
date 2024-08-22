from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin

class PIExemption(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):
    
    '''
    model handles records of exemptions granted to PIs.
    '''
    
    exemption_reason = models.CharField(max_length=255)
    
    exempted_until = models.DateField(null=True, blank=True)
    
    granted_by = models.CharField(max_length=255)
    
    granted_date = models.DateTimeField(auto_now_add=True)
    
    additional_notes = models.TextField(null=True, blank=True)