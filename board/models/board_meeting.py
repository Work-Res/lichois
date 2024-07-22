from django.db import models
from base_module.model_mixins import BaseUuidModel

from ..choices import BOARD_MEETING_TYPES, BOARD_MEETING_STATUS
from .board import Board


class BoardMeeting(BaseUuidModel):
    title = models.CharField(max_length=200)
    meeting_date = models.DateField()
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()
    description = models.CharField(max_length=150)
    status = models.CharField(max_length=50, choices=BOARD_MEETING_STATUS)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    minutes = models.TextField(blank=True, null=True)
    meeting_type = models.CharField(max_length=200, choices=BOARD_MEETING_TYPES)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title},  {self.meeting_date}"

    class Meta:
        app_label = "board"
