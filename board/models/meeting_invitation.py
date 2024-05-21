from django.db import models
import uuid

from base_module.model_mixins import BaseUuidModel

from .board_meeting import BoardMeeting
from .board_member import BoardMember
from ..choices import MEETING_INVITATION_STATUS


class MeetingInvitation(BaseUuidModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	board_meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
	invited_user = models.ForeignKey(BoardMember, on_delete=models.CASCADE, related_name='received_invitations')
	timestamp = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=MEETING_INVITATION_STATUS, default='pending')  # Possible values:
	
	def __str__(self):
		return f"Invitation to {self.meeting_title}"
