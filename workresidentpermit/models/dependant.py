from django.db import models
from app.models import ApplicationBaseModel
from ..choices import GENDER, YES_NO


class Dependant(ApplicationBaseModel):
    name = models.CharField(max_length=150)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=6, choices=GENDER)

    applying_for_residence = models.CharField(max_length=3, choices=YES_NO)
