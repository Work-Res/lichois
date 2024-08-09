from django.db import models
from app.models import ApplicationBaseModel
from app_personal_details.models.person import Person


class TravelCertificate(ApplicationBaseModel):
    kraal_head_name = models.CharField(max_length=200)
    chief_name = models.CharField(max_length=200)
    clan_name = models.CharField(max_length=200)
    date_issued = models.DateField(auto_now=True)
    father = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="father",
        null=True,
        blank=True,
    )
    mother = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="mother",
        null=True,
        blank=True,
    )
    names_of_other_relatives = models.CharField(max_length=200)
    issuing_authority = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Travel Certificate"
        verbose_name_plural = "Travel Certificates"
