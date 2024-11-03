from django.db import models
from base_module.model_mixins import BaseUuidModel

from .permissions import BoardBasePermissionModel
from .region import Region


class Board(BaseUuidModel, BoardBasePermissionModel):
    name = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.region}"

    class Meta:
        app_label = "board"
