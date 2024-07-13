from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import AGENDA_STATUS
from .board_meeting import BoardMeeting
from .application_batch import ApplicationBatch


class Agenda(BaseUuidModel):
    meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=AGENDA_STATUS, default="pending")
    notes = models.TextField(blank=True, null=True)
    application_batch = models.ForeignKey(
        ApplicationBatch,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
