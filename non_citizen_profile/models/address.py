from django.db import models
from app_address.models import Country
from app_address.choices import ADDRESS_TYPE, ADDRESS_STATUS
from identifier.non_citizen_identifier_model_mixins import (
    NonUniqueNonCitizenIdentifierModelMixin,
)


class Address(NonUniqueNonCitizenIdentifierModelMixin, models.Model):
    document_number = models.CharField(max_length=190)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.CharField(max_length=200, blank=True, null=True)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    address_type = models.CharField(
        max_length=50, choices=ADDRESS_TYPE, default="default_address_type"
    )
    status = models.CharField(max_length=50, choices=ADDRESS_STATUS, default="active")
    private_bag = models.CharField(max_length=100, blank=True, null=True)
    po_box = models.CharField(max_length=100, blank=True, null=True)
