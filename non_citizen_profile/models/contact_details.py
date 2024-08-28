from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierModelMixin,
)


class ContactDetails(models.Model, UniqueNonCitizenIdentifierModelMixin):
    document_number = models.CharField(max_length=190)
    # review model:  base_module, simple history
    telphone = models.IntegerField()
    cellphone = models.IntegerField()
    alt_cellphone = models.IntegerField()
    email = models.EmailField()
    alt_email = models.EmailField()
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)
