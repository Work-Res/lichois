from django.db import models
from ..models import Board
from base_module.model_mixins import BaseUuidModel


class VotingProcess(BaseUuidModel):
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	has_started = models.BooleanField(default=False)
	has_ended = models.BooleanField(default=False)
	document_number = models.CharField(max_length=255, unique=True)
