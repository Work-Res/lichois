from django.db import models

from base_module.model_mixins import BaseUuidModel
from app.models.application_version import ApplicationVersion


class ApplicationContact(BaseUuidModel):

    creator = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    contact_type = models.CharField(max_length=255, blank=True, null=True)
    sub_type = models.CharField(max_length=255, blank=True, null=True)
    contact_value = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.contact_type} - {self.contact_value}"
