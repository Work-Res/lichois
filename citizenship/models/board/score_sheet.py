from django.db import models

from .interview import Interview
from .board_member import BoardMember

from django.db.models import JSONField


class ScoreSheet(models.Model):
    interview = models.OneToOneField(Interview, related_name='score_sheet', on_delete=models.CASCADE)
    board_member_representation = models.ForeignKey(BoardMember, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    aggregated = JSONField(default=list)
    passed = models.BooleanField()
    summary = models.TextField()

    def __str__(self):
        return f'ScoreSheet for {self.interview}'
