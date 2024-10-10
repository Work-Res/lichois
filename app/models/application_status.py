from django.db import models

from base_module.model_mixins import BaseUuidModel


class ApplicationStatus(BaseUuidModel):
    """
    Model represent the statuses of the application.

    Attributes:
        code system code represent the status.
        name (str): User friendly name for the status.
        processes (str): indicate which process does status application to. ( using commas seperated)
        valid_from (date): The start date for application Status
        valid_to (date): The end date for application Status
    """

    code = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    processes = models.TextField(null=True, blank=True)
    valid_from = models.DateField(null=False, blank=False)
    valid_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ApplicationStatuses"
