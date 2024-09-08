from django.db import models

from base_module.model_mixins import BaseUuidModel

from .application_version import ApplicationVersion
from identifier.non_citizen_identifier_model_mixins import (
    NonUniqueNonCitizenIdentifierFieldMixin,
)


class ApplicationBaseModel(NonUniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):
    """Base model class for all models using an UUID and not
    an INT for the primary key.
    """

    document_number = models.CharField(max_length=100, null=True, blank=True)
    application_version = models.ForeignKey(
        ApplicationVersion, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta(BaseUuidModel.Meta):
        abstract = True
