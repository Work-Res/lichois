from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin
    
class PresidentialDeclaration(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):

    '''
    Model tracks declarations made by the president, including the content of the declaration.
    '''    
   
    declaration_date = models.DateField()
    
    declaration_reason = models.TextField()
    
    declared_by = models.CharField(max_length=255)  
    
    declared_status = models.CharField(max_length=50, choices=[('Prohibited', 'Prohibited'), ('Under Investigation', 'Under Investigation')], default='Prohibited')
    
    official_document = models.FileField(upload_to='declarations/')  
    
    
class MovementLog(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):

    '''
    Model records the movements of PIs when they are on the run.
    '''

    location = models.CharField(max_length=255)
    
    timestamp = models.DateTimeField()
        
    observed_by = models.CharField(max_length=255)  
    
    
class Interaction(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):

    '''
    Model logs interactions between PIs and other individuals when they are on the run.
    '''   
     
    interaction_type = models.CharField(max_length=255)
    
    description = models.TextField()
    
    location = models.CharField(max_length=255)
    
    timestamp = models.DateTimeField()
    
    involved_personnel = models.CharField(max_length=255)  