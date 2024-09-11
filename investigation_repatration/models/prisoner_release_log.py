from django.db import models
from .prisoner import Prisoner


class PrisonerReleaseLog(models.Model):
    prisoners = models.ManyToManyField(Prisoner, null=True, blank=True)
    date_of_issue = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    batch_release_date = models.DateTimeField(null=True, blank=True)
    facility_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
