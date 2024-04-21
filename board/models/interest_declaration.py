from django.db import models
from base_module.model_mixins import BaseUuidModel

from .board_member import BoardMember
from .meeting_attendee import MeetingAttendee
from .agenda_item import AgendaItem
from ..choices import BOARD_RESOLUTION, INTEREST_LEVEL


class InterestDeclaration(BaseUuidModel):

    meeting_attendee = models.OneToOneField(
        MeetingAttendee,
        on_delete=models.CASCADE
    )

    agenda_item = models.ForeignKey(
        AgendaItem,
        on_delete=models.CASCADE
    )

    client_relationship = models.CharField(
        max_length=200,
        choices=INTEREST_LEVEL
    )
    
    interest_description = models.TextField()
    
    decision = models.CharField(
        max_length=50,
        choices=BOARD_RESOLUTION
    )
    
    chair_person = models.ForeignKey(
        BoardMember,
        on_delete=models.CASCADE
    )
    attendee_signature = models.CharField(max_length=250)
    date_signed = models.DateField()

    def __str__(self):
        return f'{self.meeting_attendee}'

    class Meta:
        app_label = 'board'

