from django.db import models

from .permissions import BoardBasePermissionModel
from .board_meeting import BoardMeeting
from ..models import Board
from base_module.model_mixins import BaseUuidModel

from ..choices import VOTING_PROCESS_STATUS


class VotingProcess(BaseUuidModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=VOTING_PROCESS_STATUS)
    document_number = models.CharField(max_length=255, null=True)
    board_meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
