from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierModelMixin,
)


class PersonalDetails(models.Model, UniqueNonCitizenIdentifierModelMixin):
    document_number = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    last_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190, blank=True, null=True)
    maiden_name = models.CharField(max_length=190, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=190, blank=True, null=True)
