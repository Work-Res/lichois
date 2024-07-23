from django.db import models
from base_module.model_mixins import BaseUuidModel

from django.db.models import JSONField

from .score_sheet import ScoreSheet


class ScoreSheetDetail(BaseUuidModel):
    score_sheet = models.ForeignKey(ScoreSheet, related_name='details', on_delete=models.CASCADE)
    question = models.ForeignKey('InterviewQuestion', related_name='score_sheet_details', on_delete=models.CASCADE)
    aggregated_score = models.IntegerField()
    aggregated_responses = JSONField(default=list)  # Store list of aggregated interview responses

    def __str__(self):
        return f'ScoreSheetDetail for {self.score_sheet} - {self.question}'
