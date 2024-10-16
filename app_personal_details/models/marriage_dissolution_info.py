from django.db import models
from app.models import ApplicationBaseModel


class MarriageDissolutionInfo(ApplicationBaseModel):
    country_of_dissolution = models.CharField(max_length=100)
    place_of_dissolution = models.CharField(max_length=100)
    date_of_dissolution = models.DateField()

    def __str__(self):
        return f"Marriage Dissolved in {self.place_of_dissolution}, {self.country_of_dissolution} " \
               f"on {self.date_of_dissolution}"
