from django.db import models
from base_module.model_mixins import BaseUuidModel

from .permissions import BoardBasePermissionModel
from ..choices import VOTE_STATUS
from .meeting_attendee import MeetingAttendee


class BoardMeetingVote(BaseUuidModel, BoardBasePermissionModel):
    meeting_attendee = models.ForeignKey(MeetingAttendee, on_delete=models.CASCADE)
    document_number = models.CharField(max_length=150)
    status = models.CharField(max_length=150, choices=VOTE_STATUS)
    comments = models.TextField(blank=True, null=True)
    tie_breaker = models.CharField(
        max_length=150,
        choices=VOTE_STATUS,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Vote {self.status} by Attendee {self.meeting_attendee} for Application {self.document_number}"
