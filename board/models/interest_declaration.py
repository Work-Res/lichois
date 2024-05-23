from django.db import models
from base_module.model_mixins import BaseUuidModel

from .board_member import BoardMember
from .meeting_attendee import MeetingAttendee
from ..choices import BOARD_RESOLUTION, INTEREST_LEVEL


class InterestDeclaration(BaseUuidModel):

    meeting_attendee = models.ForeignKey(
        MeetingAttendee,
        on_delete=models.SET_NULL,
        null=True
    )

    document_number = models.CharField(max_length=150, blank=True, null=True)

    client_relationship = models.CharField(
        max_length=200,
        choices=INTEREST_LEVEL
    )
    
    interest_description = models.TextField()
    
    decision = models.CharField(
        max_length=50,
        choices=BOARD_RESOLUTION
    )
    
    attendee_signature = models.BooleanField()
    date_signed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.meeting_attendee} - {self.decision}'

    class Meta:
        app_label = 'board'

