from django.db import models
from app_contact.models import ApplicationContact
from app_contact.models.choices import CONTACT_TYPES

class ContactDetails(models.Model):
    non_citizen_id = models.IntegerField(primary_key=True)
    country_code = models.ForeignKey(ApplicationContact, on_delete=models.CASCADE, blank=True, null=True)  
    contact_type = models.CharField(max_length=100, choices=CONTACT_TYPES, blank=False, null=False)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)  
