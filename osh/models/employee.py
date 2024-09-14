from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Employee(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=[
            MinValueValidator(18),  
            MaxValueValidator(65)
        ]
    )
    event_date = models.DateField()
    statement = models.CharField(max_length=255)
    signature = models.ImageField(upload_to='employee_signatures/')

    def __str__(self):
        return f"{self.name} - {self.occupation} (Age: {self.age})"
