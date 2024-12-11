from django.db import models
from app.models import ApplicationBaseModel
from .passport import Passport


class Spouse(ApplicationBaseModel):
    last_name = models.CharField(max_length=190,verbose_name="Last Name")
    first_name = models.CharField(max_length=190,verbose_name="First Name")
    middle_name = models.CharField(max_length=190, blank=True, null=True,verbose_name="Other Names")
    maiden_name = models.CharField(max_length=190, blank=True, null=True,verbose_name="Previous/Maiden Surname")
    country = models.CharField(max_length=190,verbose_name="Country of Birth of Spouse")
    place_birth = models.CharField(max_length=190,verbose_name="Place of Birth of Spouse")
    dob = models.DateField(verbose_name="Date of Birth of Spouse")
    passport = models.ForeignKey(
        Passport,
        on_delete=models.CASCADE,
        related_name="spouse_passport",
        null=True,
    )

    class Meta:
        verbose_name = "Spouse Passport"
        verbose_name_plural = "Spouses Passports"
