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
        related_name="father_details",
        verbose_name="Father",
        help_text="Select the person who is the father.",
    )
    mother = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mother_details",
        verbose_name="Mother",
        help_text="Select the person who is the mother.",
    )
    father_address = models.ForeignKey(
        ApplicationAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="father_address_details",
        verbose_name="Father's Address",
        help_text="Specify the address of the father.",
    )
    mother_address = models.ForeignKey(
        ApplicationAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mother_address_details",
        verbose_name="Mother's Address",
        help_text="Specify the address of the mother.",
    )

    class Meta:
        app_label = "app_personal_details"
        verbose_name = "Parental Detail"
        verbose_name_plural = "Parental Details"
        ordering = ["id"]

