from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin


STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Authorized', 'Authorized'),
    ('Detained', 'Detained'),
    ('Deported', 'Deported'),
    ('Released', 'Released')
]

class ProhibitedImmigrant(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):
    
    '''
    model records individuals who are restricted from entering or remaining in Botswana.
    '''
    
    name = models.CharField(max_length=255)
    
    nationality = models.CharField(max_length=100)
    
    passport_number = models.CharField(max_length=50, unique=True)
    
    date_of_birth = models.DateField()
    
    gender = models.CharField(max_length=10)
    
    entry_date = models.DateTimeField(null=True, blank=True)  
    
    reason_for_prohibition = models.TextField()  
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    additional_notes = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"{self.name} ({self.passport_number}) - {self.nationality}"
