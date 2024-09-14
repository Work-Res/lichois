from django.db import models

class Qualification(models.Model):
    name = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)
    completion_date = models.DateField()