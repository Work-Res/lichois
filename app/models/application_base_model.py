from django.db import models

from base_module.model_mixins import BaseUuidModel

from .application_version import ApplicationVersion


class ApplicationBaseModel(BaseUuidModel):
    """Base model class for all models using an UUID and not
    an INT for the primary key.
    """

    document_number = models.CharField(max_length=100)
    application_version = models.ForeignKey(
        ApplicationVersion, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta(BaseUuidModel.Meta):
        abstract = True
