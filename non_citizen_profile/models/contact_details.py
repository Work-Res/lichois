from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class ContactDetails(UniqueNonCitizenIdentifierFieldMixin, models.Model):
    document_number = models.CharField(max_length=190, null=True, blank=True)
    telphone = models.CharField(null=True, blank=True, max_length=20)
    cellphone = models.CharField(max_length=20)
    alt_cellphone = models.CharField(null=True, blank=True, max_length=20)
    email = models.EmailField(null=True, blank=True, max_length=20)
    alt_email = models.EmailField(null=True, blank=True, max_length=120)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=20)
