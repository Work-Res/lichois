from django.db import models
from base_module.model_mixins import BaseUuidModel

from .permissions import BoardBasePermissionModel
from .board_member import BoardMember
from .board_meeting import BoardMeeting
from ..choices import ATTENDANCE_STATUS


class MeetingAttendee(BaseUuidModel, BoardBasePermissionModel):

    meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)

    board_member = models.ForeignKey(BoardMember, on_delete=models.CASCADE)

    attendance_status = models.CharField(
        choices=ATTENDANCE_STATUS, max_length=15, blank=True, null=True
    )

    def __str__(self):
        return f"{self.board_member}"

    class Meta:
        app_label = "board"
        unique_together = (
            "meeting",
            "board_member",
        )
