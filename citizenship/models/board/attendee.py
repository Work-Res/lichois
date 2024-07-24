from django.db import models

from .board_member import BoardMember
from citizenship.models.board.meeting import Meeting

from base_module.model_mixins import BaseUuidModel


class Attendee(BaseUuidModel):

    meeting = models.ForeignKey(Meeting, related_name='meetings', on_delete=models.CASCADE)
    member = models.ForeignKey(BoardMember, related_name='members', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    proposed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.member.user.username} - {self.meeting.title}'

    class Meta:
        unique_together = ('meeting', 'member')
