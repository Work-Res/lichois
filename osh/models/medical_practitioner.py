from django.db import models

class MedicalPractitioner(models.Model):
    name = models.CharField(max_length=200)
    hospital_name = models.CharField(max_length=200)