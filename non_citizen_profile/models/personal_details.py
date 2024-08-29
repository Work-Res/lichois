from django.db import models

from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class PersonalDetails(UniqueNonCitizenIdentifierFieldMixin, models.Model):
    document_number = models.CharField(max_length=190, null=True, blank=True)
    first_name = models.CharField(max_length=190)
    last_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190, blank=True, null=True)
    maiden_name = models.CharField(max_length=190, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=190, blank=True, null=True)
