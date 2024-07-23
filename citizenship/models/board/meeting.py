from django.db import models

from .choices import STATUS_CHOICES

from base_module.model_mixins import BaseUuidModel


class Meeting(BaseUuidModel):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    agenda = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')

    def __str__(self):
        return self.title
