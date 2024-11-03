from django.db import models
from base_module.model_mixins import BaseUuidModel

from .permissions import BoardBasePermissionModel
from .board import Board
from authentication.models import User


class BoardMember(BaseUuidModel, BoardBasePermissionModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="board_members",
    )
    board_join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        app_label = "board"
