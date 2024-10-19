from django.db import models


class ResidentialPlace(models.Model):
    place = models.CharField(max_length=255)  # Residential place name
    from_year = models.PositiveIntegerField()  # Year started living in the place
    to_year = models.PositiveIntegerField()    # Year ended living in the place (can be null for current place)

    def __str__(self):
        return f"{self.place} ({self.from_year} - {self.to_year if self.to_year else 'Present'})"
