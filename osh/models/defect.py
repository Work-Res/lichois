from django.db import models

class Defect(models.Model):
    description = models.TextChoices()
    remedial_action = models.TextChoices()
    safe_working_load = models.IntegerField()