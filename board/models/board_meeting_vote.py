from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..choices import VOTE_STATUS
from .meeting_attendee import MeetingAttendee
from .application import Application


class BoardMeetingVote(BaseUuidModel):
	meeting_attendee = models.ForeignKey(MeetingAttendee, on_delete=models.CASCADE)
	application = models.ForeignKey(Application, on_delete=models.CASCADE)
	status = models.CharField(max_length=150, choices=VOTE_STATUS)
	comments = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return f'Vote {self.status} by Attendee {self.attendee} for Application {self.application}'
