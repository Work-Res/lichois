from django.db import models

from app.models import Application
from citizenship.models.board import Member
from citizenship.models.board.meeting_session import MeetingSession


class Interview(models.Model):

    meeting_session = models.ForeignKey(MeetingSession, related_name='applications', on_delete=models.CASCADE)
    application = models.OneToOneField(Application, related_name='applications', on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(Member, related_name='completed_interviews')
    scheduled_time = models.DateTimeField()
    conducted = models.BooleanField(default=False)

    def __str__(self):
        return f'Interview for {self.batch_application.application.full_name()} at {self.scheduled_time}'
