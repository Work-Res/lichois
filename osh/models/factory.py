from django.db import models

class Factory(models.Model):
    name = models.CharField(max_length=255)  
    registration_no = models.CharField(max_length=100, unique=True)  
    previous_occupier = models.CharField(max_length=255, blank=True, null=True)  
    was_premise_factory_before = models.BooleanField(default=False)  
    is_staff_shifting = models.BooleanField(default=False)  
    max_hours_per_shift = models.IntegerField() 
    no_female_employees = models.IntegerField()  
    no_male_employees = models.IntegerField() 
    total_employee_no = models.IntegerField() 
    is_mechanical_power_used = models.BooleanField(default=False)  
    mechanical_power_nature = models.CharField(max_length=255, blank=True, null=True)  
    work_nature = models.CharField(max_length=50)  
