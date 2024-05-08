from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class SpouseInfo(PersonalDetailsModelMixin, BaseUuidModel):

    marriage_place = models.CharField(max_length=190,blank=True,null=True)

    spouse_death_country = models.CharField(max_length=190,blank=True,null=True)

    spouse_death_date = models.DateField(blank=True,null=True)

    academic_profession = models.TextField(max_length=190,blank=True,null=True)

    qualification_description = models.TextField(max_length=190,blank=True,null=True)

    spouse_occupation = models.CharField(max_length=190,blank=True,null=True)

    marriage_dissolution_country = models.CharField(max_length=190,blank=True,null=True)

    marriage_dissolution_place = models.CharField(max_length=190,blank=True,null=True)

    marriage_dissolution_date = models.DateField(blank=True,null=True)

    #postal_address
    #residential_address

    class Meta:
        app_label = 'citizenship'
