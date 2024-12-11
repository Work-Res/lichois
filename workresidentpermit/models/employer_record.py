from django.db import models
from app.models import ApplicationBaseModel


class EmploymentRecord(ApplicationBaseModel, models.Model):

    employer = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    duration = models.IntegerField()
    names_of_trainees = models.TextField()

    class Meta:
        app_label = "workresidentpermit"
        verbose_name = "Employment Record"
