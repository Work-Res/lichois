from django.db import models
from app.models import ApplicationBaseModel
from .passport import Passport


class Spouse(ApplicationBaseModel):
    last_name = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190, blank=True, null=True)
    maiden_name = models.CharField(max_length=190, blank=True, null=True)
    country = models.CharField(max_length=190)
    place_birth = models.CharField(max_length=190)
    country_of_death = models.CharField(max_length=190)
    place_of_death = models.CharField(max_length=190)
    date_of_death = models.DateField()
    academic_qualification = models.CharField(max_length=190)
    qualification_description = models.CharField(max_length=190)
    spouse_occupation = models.CharField(max_length=190)
    
    dob = models.DateField()
    passport = models.ForeignKey(
        Passport,
        on_delete=models.CASCADE,
        related_name="spouse_passport",
        null=True,
    )

    class Meta:
        verbose_name = "Spouse"
        verbose_name_plural = "Spouses"
