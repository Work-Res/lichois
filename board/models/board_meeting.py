from django.db import models
from base_module.model_mixins import BaseUuidModel

from ..choices import BOARD_MEETING_TYPES, BOARD_MEETING_STATUS
from .board import Board


class BoardMeeting(BaseUuidModel):
    title = models.CharField(max_length=200, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    meeting_start_time = models.TimeField(blank=True, null=True)
    meeting_end_time = models.TimeField(blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=50, choices=BOARD_MEETING_STATUS)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    minutes = models.TextField(blank=True, null=True)
    meeting_type = models.CharField(
        max_length=200,
        choices=BOARD_MEETING_TYPES,
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title},  {self.meeting_date}"

    class Meta:
        app_label = "board"
