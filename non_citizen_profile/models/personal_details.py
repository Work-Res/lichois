from django.db import models

class PersonalDetails(models.Model):
    non_citizen_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=190)
    last_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190, blank=True, null=True)
    maiden_name = models.CharField(max_length=190, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)  
    
    occupation = models.CharField(max_length=190, blank=True, null=True)  
    
