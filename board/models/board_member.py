from django.db import models
from base_module.model_mixins import BaseUuidModel
from .board import Board
from ..choices import BOARD_ROLES


class BoardMember(BaseUuidModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=250, verbose_name='User ID')
    role = models.CharField(max_length=100, choices=BOARD_ROLES)
    board_join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'BoardMember {self.user_id} - Role {self.role} at Board {self.board}'

    class Meta:
        app_label = 'board'
