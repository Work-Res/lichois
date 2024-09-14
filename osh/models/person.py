from django.db import models

class Person(models.Model):
    TYPE_CHOICES = [
        ('APPLICANT', 'Applicant'),
        ('OCCUPIER', 'Occupier'),
        ('OWNER', 'Owner'),
    ]

    type = models.CharField(
        choices=TYPE_CHOICES, 
        default='APPLICANT', 
        max_length=20
    )
    name = models.CharField(max_length=200)
    age = models.IntegerField(blank=True, null=True)  
    education_outline = models.TextField(blank=True)  
    present_occupation = models.CharField(max_length=200, blank=True)  

