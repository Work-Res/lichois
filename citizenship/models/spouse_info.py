from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class SpouseInfo(PersonalDetailsModelMixin, BaseUuidModel):

    spouse_death_country = models.CharField(max_length=190)

    spouse_death_date = models.DateField()

    academic_profession = models.TextField(max_length=190)

    qualification_description = models.TextField(max_length=190)

    spouse_occupation = models.CharField(max_length=190)

    marriage_dissolution_country = models.CharField(max_length=190)

    marriage_dissolution_place = models.CharField(max_length=190)

    marriage_dissolution_date = models.DateField()

    class Meta:
        app_label = 'citizenship'
