from django.db import models

from app.models import ApplicationBaseModel


class Passport(ApplicationBaseModel):

    passport_number = models.CharField(verbose_name="Passport number", max_length=15)

    date_issued = models.DateField(
        verbose_name="Date of issue"
        # validation=date_not_future
    )

    place_issued = models.CharField(verbose_name="Country of issue", max_length=190)

    expiry_date = models.DateField(
        verbose_name="Date of expiry"
        # validation=date_not_past
    )

    nationality = models.CharField(
        max_length=190,
        verbose_name="Nationality(State name of country)"
    )

    photo = models.URLField()

    previous_passport_number = models.CharField(
        max_length=190,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Passport"
