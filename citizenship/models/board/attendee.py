from django.db import models

from citizenship.models.board.meeting import Meeting
from citizenship.models.board.meeting_session import MeetingSession
from citizenship.models.board.member import Member


class Attendee(models.Model):
    session = models.ForeignKey(MeetingSession, related_name='attendees', on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, related_name='attendees', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='attendances', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.member.user.username} - {self.meeting.title}'
