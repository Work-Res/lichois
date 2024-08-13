from django.db import models

from ..choices import MARITAL_STATUS, GENDER, PERSON_TYPE

from app.models import ApplicationBaseModel


class Person(ApplicationBaseModel):

    first_name = models.CharField(max_length=190)

    last_name = models.CharField(max_length=190)

    middle_name = models.CharField(max_length=190, blank=True, null=True)

    maiden_name = models.CharField(max_length=190, blank=True, null=True)

    marital_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=MARITAL_STATUS,
    )

    dob = models.DateField(
        blank=True,
        null=True,
        # validations=date_not_future TODO: add validation (more than 18 years only )
    )

    country_birth = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    place_birth = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        blank=True,
        null=True,
    )

    occupation = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    qualification = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    person_type = models.CharField(
        max_length=150,
        choices=PERSON_TYPE,
        default="applicant",
    )

    decreased = models.BooleanField(default=False)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Personal Details"
        verbose_name_plural = "Personal Details"
