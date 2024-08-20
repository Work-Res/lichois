from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier import UniqueNonCitizenIdentifierFieldMixin

status_choices = [
        ('INCARCERATED', 'Incarcerated'),
        ('RELEASED', 'Released'),
        ('TRANSFERRED', 'Transferred'),
    ]


class Prisoner(
        UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    # Incarceration Details
    incarceration_date = models.DateField()

    release_date = models.DateField(blank=True, null=True)

    crime_committed = models.TextField()

    sentence_years = models.PositiveIntegerField()

    status = models.CharField(
        max_length=12,
        choices=status_choices,
        default='INCARCERATED')

    @property
    def first_name(self):
        #TODO: impiment the property
        return ''

    @property
    def last_name(self):
        #TODO: impiment the property
        return ''

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.non_citizen_identifier}"
