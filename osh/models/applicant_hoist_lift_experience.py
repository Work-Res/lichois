from django.db import models

class ApplicantHoistLiftExperience(models.Model):
    type_choices = [
        ('HOIST', 'Hoist'),
        ('LIFT','Lift')
    ]

    type = models.CharField(
        choices = type_choices,
        max_length = 50,
        default = 'HOIST'
    )
    description = models.TextChoices()