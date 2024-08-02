from django.db import models

from .choices import BATCH_STATUS_CHOICES

from base_module.model_mixins import BaseUuidModel


class Batch(BaseUuidModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=BATCH_STATUS_CHOICES, default='IN_PROGRESS')
    date_of_publish = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.meeting.title}'
