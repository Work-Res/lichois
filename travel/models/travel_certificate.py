from django.db import models
from app.models import ApplicationBaseModel
from app_personal_details.models.person import Person


class TravelCertificate(ApplicationBaseModel):
    kraal_head_name = models.CharField(
        max_length=200,
        verbose_name="Kraal Head Name",
        help_text="Enter the name of the kraal head.",
    )
    chief_name = models.CharField(
        max_length=200,
        verbose_name="Chief Name",
        help_text="Enter the name of the chief.",
    )
    clan_name = models.CharField(
        max_length=200,
        verbose_name="Clan Name",
        help_text="Enter the name of the clan.",
    )
    date_issued = models.DateField(
        auto_now=True,
        verbose_name="Date Issued",
        help_text="The date the travel certificate was issued.",
    )
    mother_full_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Mother's Full Address",
        help_text="Enter the full address of the mother.",
    )
    names_of_other_relatives = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Names of Other Relatives",
        help_text="Enter the names of other relatives.",
    )
    full_address_of_relative = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Full Address of Relative",
        help_text="Enter the full address of the relative.",
    )
    original_home_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Original Home Address",
        help_text="Enter the original home address.",
    )
    issuing_authority = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Issuing Authority",
        help_text="Enter the name of the authority that issued the certificate.",
    )

    class Meta:
        app_label = "app"
        verbose_name = "Travel Certificate"
        verbose_name_plural = "Travel Certificates"
        ordering = ["-date_issued"]

    def __str__(self):
        return f"Travel Certificate issued to {self.kraal_head_name} by {self.issuing_authority or 'Unknown Authority'} on {self.date_issued}"
