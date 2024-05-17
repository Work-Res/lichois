from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import BOARD_MEETING_TYPES, BOARD_MEETING_STATUS
from .board import Board


class BoardMeeting(BaseUuidModel):
	title = models.CharField(max_length=200)
	meeting_date = models.DateTimeField()
	description = models.CharField(max_length=150)
	status = models.CharField(max_length=50, choices=BOARD_MEETING_STATUS)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	minutes = models.TextField(blank=True, null=True)
	meeting_type = models.CharField(max_length=200, choices=BOARD_MEETING_TYPES)
	location = models.CharField(max_length=200)
	
	def __str__(self):
		return (f'{self.meeting_type},  {self.meeting_date},'
		        f'{self.board_id}')
	
	class Meta:
		app_label = 'board'
