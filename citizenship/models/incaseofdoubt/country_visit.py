from django.db import models


class CountryVisit(models.Model):
    country = models.CharField(max_length=255)  # Name of the country visited
    reason = models.CharField(max_length=255)   # Reason for the visit
    year = models.PositiveIntegerField()        # Year of the visit

    def __str__(self):
        return f"{self.country} ({self.year}) - Reason: {self.reason}"
