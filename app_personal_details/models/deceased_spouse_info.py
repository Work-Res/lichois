from django.db import models
from app.models import ApplicationBaseModel


class DeceasedSpouseInfo(ApplicationBaseModel):

    country_of_death = models.CharField(max_length=100)
    place_of_death = models.CharField(max_length=100)
    date_of_death = models.DateField()

    def __str__(self):
        return f"Deceased Spouse (Died in {self.place_of_death}, {self.country_of_death} on {self.date_of_death})"
