from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import AGENDA_STATUS
from .board_meeting import BoardMeeting
from .agenda_item import AgendaItem
from .application_batch import ApplicationBatch


class Agenda(BaseUuidModel):
	meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
	description = models.TextField()
	duration = models.DurationField()
	status = models.CharField(max_length=50, choices=AGENDA_STATUS, default='pending')
	notes = models.TextField(blank=True, null=True)
	agenda_items = models.ManyToManyField(AgendaItem)
	application_batch = models.ForeignKey(ApplicationBatch, on_delete=models.CASCADE, blank=True, null=True)
