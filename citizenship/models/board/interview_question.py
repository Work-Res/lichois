from django.db import models

from citizenship.models.board import Question
from citizenship.models.board.interview import Interview


class InterviewQuestion(models.Model):
    interview = models.ForeignKey(Interview, related_name='questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='interview_questions', on_delete=models.CASCADE)
    score = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    is_marked = models.BooleanField()

    def __str__(self):
        return f'Question: {self.question.text}'
