from django.db import models

from ..choices import MARITAL_STATUS, GENDER, PERSON_TYPE

from app.models import ApplicationBaseModel
from base_module.model_mixins import NationalityModelMixin


class Person(ApplicationBaseModel, NationalityModelMixin, models.Model):

    first_name = models.CharField(max_length=190, verbose_name='First Name', )

    last_name = models.CharField(max_length=190, verbose_name='Surname')

    other_names = models.CharField(max_length=255, null=True, blank=True, verbose_name='Other Names')

    maiden_name = models.CharField(max_length=190, blank=True, null=True, verbose_name='Previous/Maiden Surname')

    marital_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=MARITAL_STATUS, verbose_name='Marital Status'
    )

    dob = models.DateField(
        verbose_name='Date of Birth',
        blank=True,
        null=True,
        # validations=date_not_future TODO: add validation (more than 18 years only )
    )

    person_type = models.CharField(
        max_length=150,
        choices=PERSON_TYPE,
        default="applicant",
    )

    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        verbose_name='Sex',
    )

    occupation = models.CharField(
        max_length=190,
        blank=True,
        null=True,verbose_name='Occupation',
    )

    qualification = models.CharField(
        max_length=190,
        blank=True,
        null=True, verbose_name='Qualification',
    )


    def full_name(self):
        return f"{self.first_name} {self.other_names} {self.last_name}"

    class Meta:
        verbose_name = "Personal Details"
        verbose_name_plural = "Personal Details"
