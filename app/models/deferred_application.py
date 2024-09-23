from django.db import models

from . import ApplicationStatus
from .application import Application

from base_module.model_mixins import BaseUuidModel


class DeferredApplication(BaseUuidModel):

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    deferred_from = models.CharField(max_length=100)
    expected_action = models.CharField(max_length=100, null=True, blank=True)
    deferred_status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "DeferredApplications"
