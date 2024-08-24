from django.db import models

from .interview import Interview
from .board_member import BoardMember

from django.db.models import JSONField


class ScoreSheet(models.Model):
    interview = models.OneToOneField(
        Interview, related_name="score_sheet", on_delete=models.CASCADE
    )
    board_member_representation = models.ForeignKey(
        BoardMember, on_delete=models.CASCADE, null=True, blank=True
    )
    total_score = models.IntegerField()
    average_score = models.IntegerField()
    aggregated = JSONField(default=list, null=True, blank=True)
    passed = models.BooleanField()
    summary = models.TextField(null=True, blank=True)
    recording = models.FileField(upload_to="recordings/", null=True, blank=True)
    document = models.FileField(upload_to="documents/", null=True, blank=True)

    def __str__(self):
        return f"ScoreSheet for {self.interview}"
