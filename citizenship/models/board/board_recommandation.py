from django.db import models

from .score_sheet import ScoreSheet


class BoardRecommendation(models.Model):
    score_sheet = models.OneToOneField(ScoreSheet, related_name='board_recommendation', on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=20, choices=[('Granted', 'Granted'), ('Denied', 'Denied')], default='Granted')
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Recommendation for {self.score_sheet.interview.batch_application.application.applicant_name}'
