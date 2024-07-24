from django.db import models

from django.utils import timezone

from .choices import STATUS_CHOICES

from base_module.model_mixins import BaseUuidModel

from .board import Board


class Meeting(BaseUuidModel):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    location = models.CharField(max_length=200)
    agenda = models.TextField()
    board = models.ForeignKey(Board, related_name='board_meetings', on_delete=models.CASCADE)  # New field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title
