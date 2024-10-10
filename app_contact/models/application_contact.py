from django.db import models

from app.models import ApplicationBaseModel

from .choices import CONTACT_TYPES
from django.core.validators import MinValueValidator, MaxValueValidator


class ApplicationContact(ApplicationBaseModel):

    creator = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    contact_type = models.CharField(choices=CONTACT_TYPES, max_length=100, blank=False, null=False)
    sub_type = models.CharField(max_length=255, blank=True, null=True)
    contact_value = models.CharField(max_length=255, blank=False, null=False)
    preferred_method_comm = models.BooleanField(default=False)
    email = models.EmailField()
    cell = models.CharField(max_length=20)

    def __str__(self):
        return f" {self.contact_type} - {self.contact_value}"
