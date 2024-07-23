from django.db import models

from authentication.models import User
from citizenship.models.board import Board
from citizenship.models.board.role import Role


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='members', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.board.name}'
