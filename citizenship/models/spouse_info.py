from django.db import models
from base_module.choices import YES_NO
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class SpouseInfo(PersonalDetailsModelMixin, BaseUuidModel):

    marriage_place = models.CharField(max_length=190, blank=True,null=True)
    spouse_death_country = models.CharField(max_length=190, blank=True, null=True)
    spouse_death_date = models.DateField(blank=True, null=True)
    academic_profession = models.TextField(max_length=190, blank=True, null=True)
    marriage_dissolution_country = models.CharField(max_length=190, blank=True ,null=True)
    marriage_dissolution_place = models.CharField(max_length=190, blank=True, null=True)
    marriage_dissolution_date = models.DateField(blank=True, null=True)
    spouse_citizenship_acquired = models.CharField(max_length=190, blank=True, null=True)
    marriage_subsisting = models.CharField(choices=YES_NO, max_length=5, blank=True, null=True)

    #postal_address
    #residential_address

    class Meta:
        app_label = 'citizenship'
