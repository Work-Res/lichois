from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class PrisonerDueForRelease(BaseUuidModel):

    start_release_date = models.DateField()

    end_release_date = models.DateField()


class PrisonerDetails(UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    due_release = models.ForeignKey(PrisonerDueForRelease, on_delete=models.CASCADE)

    fullnames = models.CharField(max_length=255)

    dob = models.DateField()  # Date of Birth

    gender = models.CharField(max_length=10)

    nationality = models.CharField(max_length=100)

    offense = models.TextField()

    sentence = models.TextField()

    case_no = models.CharField(max_length=100, unique=True)

    date_of_release = models.DateField()
