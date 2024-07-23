from django.db import models

from base_module.model_mixins import BaseUuidModel

from .interview import Interview
from .interview_question import InterviewQuestion
from .board_member import BoardMember


class InterviewResponse(BaseUuidModel):
    interview = models.ForeignKey(Interview, related_name='completed_interviews', on_delete=models.CASCADE)
    question = models.ForeignKey(InterviewQuestion, related_name='interview_questions', on_delete=models.CASCADE)
    member = models.ForeignKey(BoardMember, related_name='panel_members', on_delete=models.CASCADE)
    response = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    is_marked = models.BooleanField(default=False)
    # recording = models.FileField(upload_to='recordings/', null=True, blank=True) belong to the score-sheet

    def __str__(self):
        return f'{self.interview} - {self.question}'
