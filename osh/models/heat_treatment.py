from django.db import models
from .inspector import Inspector

class HeatTreatment(models.Model):
    date = models.DateField()
    done_by = models.ForeignKey(Inspector, on_delete=models.SET_NULL)