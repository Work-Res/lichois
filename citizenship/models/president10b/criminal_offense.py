from django.db import models

from base_module.model_mixins import BaseUuidModel


class CriminalOffense(BaseUuidModel):

    offense_description = models.TextField()
    date_of_conviction = models.DateField()
    country_of_offense = models.CharField(max_length=100)
    penalty_given = models.CharField(max_length=255)

    def __str__(self):
        return f"Offense: {self.offense_description} in {self.country_of_offense} on {self.date_of_conviction}"