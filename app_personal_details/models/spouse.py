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
    dob = models.DateField()
    passport = models.ForeignKey(
        Passport,
        on_delete=models.CASCADE,
        related_name="spouse_passport",
        null=True,
    )
    # place_issued = models.ForeignKey(
    #     Passport,
    #     on_delete=models.CASCADE,
    #     related_name="spouse_place_issued",
    #     null=True,
    # )
    # date_issued = models.ForeignKey(
    #     Passport,
    #     on_delete=models.CASCADE,
    #     related_name="spouse_date_issued",
    #     null=True,
    # )
    # expiry_date = models.ForeignKey(
    #     Passport,
    #     on_delete=models.CASCADE,
    #     related_name="spouse_expiry_date",
    #     null=True,
    # )
    # nationality = models.ForeignKey(
    #     Passport,
    #     on_delete=models.CASCADE,
    #     related_name="spouse_nationality",
    #     null=True,
    # )

    class Meta:
        verbose_name = "Spouse"
        verbose_name_plural = "Spouses"
