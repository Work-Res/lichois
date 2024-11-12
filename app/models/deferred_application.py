from django.db import models

from . import ApplicationStatus
from .application import Application
from base_module.model_mixins import BaseUuidModel


class DeferredApplication(BaseUuidModel):
    previous_application_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.CASCADE,
        related_name="deferred_applications_previous",
        null=True,
        blank=True
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="deferred_applications"
    )
    comment = models.TextField(blank=True, null=True)
    deferred_from = models.CharField(max_length=100)
    expected_action = models.CharField(max_length=100, null=True, blank=True)
    deferred_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.CASCADE,
        related_name="deferred_applications_status"
    )

    class Meta:
        verbose_name_plural = "Deferred Applications"

    def __str__(self):
        return f"DeferredApplication for {self.application} from {self.deferred_from}"