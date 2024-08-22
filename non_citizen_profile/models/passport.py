from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import  NonUniqueNonCitizenIdentifierFieldMixin

class Passport(BaseUuidModel, NonUniqueNonCitizenIdentifierFieldMixin):
    
    non_citizen_id = models.IntegerField(primary_key=True)
    
    passport_number = models.CharField(verbose_name="Passport number", max_length=15)
    
    date_issued = models.DateField(verbose_name="Date of issue")
    
    place_issued = models.CharField(max_length=200, verbose_name="Country of issue")
    
    expiry_date = models.DateField(verbose_name="Date of expiry")
    
    nationality = models.CharField(max_length=190)
    
    photo = models.URLField()