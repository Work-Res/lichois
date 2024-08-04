from django.db import models

from base_module.model_mixins import BaseUuidModel

from .interview import Interview
from .board_member import BoardMember


class InterviewResponse(BaseUuidModel):
    interview = models.ForeignKey(Interview, related_name='completed_interviews', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    member = models.ForeignKey(BoardMember, related_name='panel_members', on_delete=models.CASCADE)
    response = models.TextField()
    marks_range = models.CharField(max_length=200)
    score = models.IntegerField(null=True, blank=True)
    is_marked = models.BooleanField(null=True, blank=True)
    additional_comments = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200)
    # recording = models.FileField(upload_to='recordings/', null=True, blank=True) belong to the score-sheet

    def __str__(self):
        return f'{self.interview} - {self.text}'
