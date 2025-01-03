from django.db import models

from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class Passport(UniqueNonCitizenIdentifierFieldMixin, models.Model):
    passport_number = models.CharField(verbose_name="Passport number", max_length=15)
    date_issued = models.DateField(verbose_name="Date of issue")
    place_issued = models.CharField(max_length=200, verbose_name="Country of issue")
    expiry_date = models.DateField(verbose_name="Date of expiry")
    nationality = models.CharField(max_length=190)
    photo = models.URLField()
    document_number = models.CharField(max_length=190, null=True, blank=True)
