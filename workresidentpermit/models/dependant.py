from django.db import models
from app.models import ApplicationBaseModel
from ..choices import GENDER


class Dependant(ApplicationBaseModel):
	name = models.CharField(max_length=150)
	
	age = models.PositiveIntegerField(max_length=150)
	
	gender = models.CharField(max_length=6, choices=GENDER)
