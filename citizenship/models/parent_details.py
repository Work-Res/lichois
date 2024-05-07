from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin
from ..choices import PARENT_TYPE


class ParentDetails(PersonalDetailsModelMixin, BaseUuidModel):

    parent_type = models.CharField(
        max_length=15, choices=PARENT_TYPE
    )

    death_citizenship = models.CharField(max_length=190, blank=True, null=True)

    #postal_address

    #residential_address

    dob = models.DateField(blank=True, null=True)

    birth_place = models.CharField(max_length=190, blank=True, null=True)

    nationality = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        app_label = 'citizenship'

