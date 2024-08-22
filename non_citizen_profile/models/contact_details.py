from django.db import models
from base_module.model_mixins import BaseUuidModel


class ContactDetails(BaseUuidModel, models.Model):
    
    non_citizen_id = models.IntegerField(primary_key=True)
    
    telphone = models.IntegerField()
    
    cellphone = models.IntegerField()
    
    alt_cellphone = models.IntegerField()
    
    email = models.EmailField()
    
    alt_email = models.EmailField()
    
    emergency_contact_name = models.CharField(max_length=200)
    
    emergency_contact_number = models.CharField(max_length=15)  