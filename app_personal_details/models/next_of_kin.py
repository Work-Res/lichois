from django.db import models

from app.models.application_base_model import ApplicationBaseModel


class NextOfKin(ApplicationBaseModel):

    first_name = models.CharField(max_length=190,verbose_name="First Name")


    last_name = models.CharField(max_length=190,verbose_name="Last Name")

    telephone = models.CharField(
        max_length=190,
        blank=True,
        null=True,
        verbose_name="Telephone"
    )

    cell_phone = models.CharField(
        max_length=190,
        blank=True,
        null=True,
        verbose_name="Cellphone"
    )

    relation = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Relations"
    )

    physical_address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Physical Address"
    )
