from base_module.model_mixins import BaseUuidModel
from django.db import models

from board.models.application_batch import ApplicationBatch

from ..choices import VOTING_PROCESS_STATUS
from ..models import Board
from .board_meeting import BoardMeeting


class VotingProcess(BaseUuidModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=VOTING_PROCESS_STATUS)
    batch = models.ForeignKey(
        ApplicationBatch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    board_meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
