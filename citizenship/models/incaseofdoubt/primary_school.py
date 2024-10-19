from django.db import models


class PrimarySchool(models.Model):
    name = models.CharField(max_length=255)
    attended_from_standard = models.IntegerField(choices=[(i, f'Standard {i}') for i in range(1, 8)])
    attended_to_standard = models.IntegerField(choices=[(i, f'Standard {i}') for i in range(1, 8)])

    def __str__(self):
        return self.name
