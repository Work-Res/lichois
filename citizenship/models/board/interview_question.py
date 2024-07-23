from django.db import models

from base_module.model_mixins import BaseUuidModel

from .meeting import Meeting


class InterviewQuestion(BaseUuidModel):
    meeting = models.ForeignKey(Meeting, related_name='interview_questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text
