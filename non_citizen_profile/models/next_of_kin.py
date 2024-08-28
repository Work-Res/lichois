from django.db import models

from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierModelMixin,
)


class NextOfKin(models.Model, UniqueNonCitizenIdentifierModelMixin):

    document_number = models.CharField(max_length=190)

    first_name = models.CharField(max_length=190)

    last_name = models.CharField(max_length=190)

    telephone = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    cell_phone = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    relation = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
