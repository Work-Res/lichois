from django.db import models
from base_module.model_mixins import BaseUuidModel
from .region import Region


class Board(BaseUuidModel):
    name = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    board_id = models.CharField(max_length=250, verbose_name='Board Identifier')

    def __str__(self):
        return f'{self.name} {self.region}'

    class Meta:
        app_label = 'board'
