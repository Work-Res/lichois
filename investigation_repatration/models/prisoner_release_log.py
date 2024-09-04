from django.db import models
from .prisoner import Prisoner


class PrisonerReleaseLog(models.Model):
    prisoners = models.ManyToManyField(Prisoner, null=True, blank=True)
