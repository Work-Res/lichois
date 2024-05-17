from django.db import models
from base_module.model_mixins import BaseUuidModel
from .board import Board
from ..choices import BOARD_ROLES
from authentication.models import User


class BoardMember(BaseUuidModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_members')
    role = models.CharField(max_length=100, choices=BOARD_ROLES)
    board_join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'BoardMember {self.user_id} - Role {self.role} at Board {self.board}'

    class Meta:
        app_label = 'board'

