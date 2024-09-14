from django.db import models

class ApplicantConstructionExperience(models.Model):
    receiver_type = models.CharField(max_length=100)
    description = models.TextChoices()
    