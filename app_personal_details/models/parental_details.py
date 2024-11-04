from django.db import models

from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from app.models import ApplicationBaseModel


class ParentalDetails(ApplicationBaseModel):
    father = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="father",
    )

    mother = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mother",
    )

    father_address = models.ForeignKey(
        ApplicationAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="father_address",
    )

    mother_address = models.ForeignKey(
        ApplicationAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mother_address",
    )
