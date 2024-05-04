from django.db import models
from base_module.model_mixins import BaseUuidModel

from .work_resident_permit import WorkResidencePermit


class PlaceOfResidence(BaseUuidModel):

    country = models.CharField(max_length=190)
    place_of_residence = models.CharField(max_length=190)
    work_resident_permit = models.ForeignKey(WorkResidencePermit, on_delete=models.CASCADE)


class SpousePlaceOfResidence(BaseUuidModel):
    country = models.CharField(max_length=190)
    place_of_residence = models.CharField(max_length=190)
    work_resident_permit = models.ForeignKey(WorkResidencePermit, on_delete=models.CASCADE)
