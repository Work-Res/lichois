from django.db import models


class SeniorHighSchool(models.Model):
    name = models.CharField(max_length=255)  # Name of the senior high school
    period_from = models.DateField()  # Date attended from (start date)
    period_to = models.DateField()    # Date attended to (end date)

    def __str__(self):
        return self.name
