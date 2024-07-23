from django.db import models

from app.models import Application

from .board_member import BoardMember

from citizenship.models.board.meeting_session import MeetingSession
from base_module.model_mixins import BaseUuidModel


class Interview(BaseUuidModel):

    meeting_session = models.ForeignKey(MeetingSession, related_name='applications', on_delete=models.CASCADE)
    application = models.OneToOneField(Application, related_name='applications', on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(BoardMember, related_name='completed_interviews')
    scheduled_time = models.DateTimeField()
    conducted = models.BooleanField(default=False)

    def __str__(self):
        return f'Interview for {self.batch_application.application.full_name()} at {self.scheduled_time}'
