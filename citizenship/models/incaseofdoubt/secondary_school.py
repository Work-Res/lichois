from django.db import models


class SecondarySchool(models.Model):
    name = models.CharField(max_length=255)  # Name of the secondary school
    period_from = models.DateField()  # Date attended from
    period_to = models.DateField()    # Date attended to

    def __str__(self):
        return self.name
