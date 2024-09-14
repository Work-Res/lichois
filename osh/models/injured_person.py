from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class InjuredPerson(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    name = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    gender = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES,  
        default='Female'
    )
    age = models.IntegerField(
        validators=[
            MinValueValidator(18),  
            MaxValueValidator(65)   
        ]
    )
    average_hourly_pay = models.IntegerField()

   