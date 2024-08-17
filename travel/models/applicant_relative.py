from django.db import models
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress


class ApplicantRelative(ApplicationBaseModel):
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=200)
    address = models.ForeignKey(ApplicationAddress, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Travel Certificate"
        verbose_name_plural = "Travel Certificates"
