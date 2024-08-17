from django.db import models
from base_module.model_mixins import BaseUuidModel

from .resident_permit import ResidencePermit


class PlaceOfResidence(BaseUuidModel):

    country = models.CharField(max_length=190)
    place_of_residence = models.CharField(max_length=190)


class SpousePlaceOfResidence(BaseUuidModel):
    country = models.CharField(max_length=190)
    place_of_residence = models.CharField(max_length=190)
