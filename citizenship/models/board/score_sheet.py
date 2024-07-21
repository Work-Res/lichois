from django.db import models

from citizenship.models.board import Interview


class ScoreSheet(models.Model):
    interview = models.OneToOneField(Interview, related_name='score_sheet', on_delete=models.CASCADE)
    total_score = models.IntegerField()
    passed = models.BooleanField()
    summary = models.TextField()

    def __str__(self):
        return f'ScoreSheet for {self.interview}'
