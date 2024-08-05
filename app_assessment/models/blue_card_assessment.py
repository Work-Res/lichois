from django.db import models

from app.models import ApplicationBaseModel


class BlueCardAssessment(ApplicationBaseModel):
    name_of_supporter = models.CharField(max_length=255)
    relationship_to_supporter = models.CharField(max_length=255)
    observations = models.TextField()
