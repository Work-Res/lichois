from django.db import models

from .choices import BATCH_STATUS_CHOICES

from citizenship.models.board.meeting import Meeting
from base_module.model_mixins import BaseUuidModel


class Batch(BaseUuidModel):

    meeting = models.ForeignKey(Meeting, related_name='batches', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=BATCH_STATUS_CHOICES, default='open')

    def __str__(self):
        return f'{self.name} - {self.meeting.title}'
