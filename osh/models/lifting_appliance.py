from django.db import models

class LiftingAppliance(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField()
    distinctive_no = models.IntegerField()
    first_use_date = models.DateField()
