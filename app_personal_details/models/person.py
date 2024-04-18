from django.db import models

from workresidentpermit.choices import MARITAL_STATUS, GENDER

from base_module.model_mixins import BaseUuidModel
from app.models import ApplicationVersion


class Person(BaseUuidModel):

    first_name = models.CharField(max_length=190)

    last_name = models.CharField(max_length=190)

    middle_name = models.CharField(
        max_length=190,
        blank=True,
        null=True)

    maiden_name = models.CharField(
        max_length=190,
        blank=True,
        null=True)

    marital_status = models.CharField(
        max_length=50,
        choices=MARITAL_STATUS)

    dob = models.DateField(
        # validations=date_not_future TODO: add validation (more than 18 years only )
    )

    country_birth = models.CharField(max_length=190)

    place_birth = models.CharField(max_length=190)

    gender = models.CharField(max_length=6, choices=GENDER)

    place_birth = models.CharField(max_length=190)

    gender = models.CharField(
        max_length=6,
        choices=GENDER)

    occupation = models.CharField(max_length=190)

    qualification = models.CharField(max_length=190)

    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Personal Details'
        verbose_name_plural = 'Personal Details'
