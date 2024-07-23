from django.db import models

from citizenship.models.board.role import Role


class Board(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100) # Fixme: make a foregin key to read from classifers..
    description = models.TextField()
    quorum_roles = models.ManyToManyField(Role, related_name='quorum_roles')

    def has_quorum(self):
        for role in self.quorum_roles.all():
            if not self.members.filter(role=role).exists():
                return False
        return True

    def __str__(self):
        return self.name
