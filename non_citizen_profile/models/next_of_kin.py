from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier.identifier import  NonUniqueNonCitizenIdentifierFieldMixin


class NextOfKin(BaseUuidModel, NonUniqueNonCitizenIdentifierFieldMixin):

    non_citizen_id = models.IntegerField(primary_key=True)

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
