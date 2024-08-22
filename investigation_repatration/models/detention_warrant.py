from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin
from app.models import ApplicationBaseModel



class DetentionWarrant(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin, ApplicationBaseModel):
    
    '''
    Model captures details about legal orders authorizing the detention of PIs.
    '''
    
    authorized_by = models.CharField(max_length=255)
    
    detention_reason = models.TextField()
    
    detention_date = models.DateTimeField(auto_now_add=True)
    
    detention_location = models.CharField(max_length=255) #not in the form
    
    release_conditions = models.TextField(null=True, blank=True) #not in the form
    
    def __str__(self):
        return f"Detention Authorization for {self.pi.name} by {self.authorized_by.name} on {self.detention_date}"
