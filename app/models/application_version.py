from django.db import models

from .application import Application

from base_module.model_mixins import BaseUuidModel


class ApplicationVersion(BaseUuidModel):
    """
    Model represent the application version, carter for revision of applications and so on.

    Attributes:
        application, foreign to linking to application.
        version_number (str): numeric number that represent version number.
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.application} - Version {self.version_number}"

    class Meta:
        verbose_name_plural = "ApplicationVersions"
