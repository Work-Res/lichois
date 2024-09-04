from django.db import models
from django.apps import apps

from base_module.model_mixins import BaseUuidModel
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)

status_choices = [
    ("INCARCERATED", "Incarcerated"),
    ("RELEASED", "Released"),
    ("TRANSFERRED", "Transferred"),
]


class Prisoner(UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    release_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=12, choices=status_choices, default="INCARCERATED"
    )

    batched = models.BooleanField(default=False)

    @property
    def first_name(self):
        if self.personal_details:
            return self.personal_details.first_name
        return None

    @property
    def last_name(self):
        if self.personal_details:
            return self.personal_details.last_name
        return None

    @property
    def personal_details(self):
        PersonalDetails = apps.get_model("non_citizen_profile.PersonalDetails")
        try:
            return PersonalDetails.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except PersonalDetails.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.non_citizen_identifier}"
