from django.db import models
from base_module.model_mixins import BaseUuidModel

from .score_sheet import ScoreSheet


class BoardRecommendation(BaseUuidModel):
    score_sheet = models.OneToOneField(
        ScoreSheet, related_name="board_recommendation", on_delete=models.CASCADE
    )
    recommendation = models.CharField(
        max_length=20,
        choices=[("Granted", "Granted"), ("Denied", "Denied")],
        default="Granted",
    )

    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Recommendation for {self.score_sheet.interview.application.full_name}"
