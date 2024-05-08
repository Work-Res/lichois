from django.db import models

from base_module.model_mixins import BaseUuidModel

from .resident_permit import ResidencePermit


class Spouse(BaseUuidModel):
    spouse_last_name = models.CharField(max_length=190)
    spouse_first_name = models.CharField(max_length=190)
    spouse_middle_name = models.CharField(max_length=190)
    spouse_maiden_name = models.CharField(max_length=190)
    spouse_country = models.CharField(max_length=190)
    spouse_place_birth = models.CharField(max_length=190)
    spouse_dob = models.DateField()
    work_resident_permit = models.ForeignKey(ResidencePermit, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Spouse'
