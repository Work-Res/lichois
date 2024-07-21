from django.db import models

from app_checklist.models import Region
from citizenship.models.board.role import Role

from base_module.model_mixins import BaseUuidModel


class Board(BaseUuidModel):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    description = models.TextField()
    quorum_roles = models.ManyToManyField(Role, related_name='quorum_roles')

    def has_quorum(self):
        for role in self.quorum_roles.all():
            if not self.members.filter(role=role).exists():
                return False
        return True

    def __str__(self):
        return self.name
