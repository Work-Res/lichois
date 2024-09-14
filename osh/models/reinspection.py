from django.db import models
from .inspector import Inspector

class Reinspection(models.Model):
    date = models.DateField()
    details = models.TextField()
    name = models.ForeignKey(Inspector, on_delete = models.CASCADE)
    