from django.db import models

from app.models import Application

from .board_member import BoardMember

from citizenship.models.board.meeting_session import MeetingSession
from base_module.model_mixins import BaseUuidModel

from .choices import INTERVIEW_STATUS_CHOICES, VARIATION_TYPE_CHOICES


class Interview(BaseUuidModel):

    meeting_session = models.ForeignKey(MeetingSession, related_name='applicant_meeting_sessions',
                                        on_delete=models.CASCADE)
    application = models.OneToOneField(Application, related_name='applications', on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(BoardMember, related_name='completed_interviews')
    scheduled_time = models.DateTimeField()
    conducted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='pending')
    variation_type = models.CharField(max_length=50, choices=VARIATION_TYPE_CHOICES, default='student')

    def __str__(self):
        return f'Interview for {self.application} at {self.scheduled_time}'
