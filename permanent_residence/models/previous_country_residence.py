from django.db import models
from app.models import ApplicationBaseModel


class PreviousCountryResidence(ApplicationBaseModel):
    country = models.CharField(max_length=255, blank=True, null=True)
    place_residence = models.CharField(max_length=255, blank=True, null=True)
    have_travelled_on_pass = models.BooleanField(max_length=255, blank=True, null=True)
