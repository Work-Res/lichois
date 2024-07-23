from django.db import models

from base_module.model_mixins import BaseUuidModel
from .interview import Interview
from .board_member import BoardMember


class InterviewDecision(BaseUuidModel):
    interview = models.ForeignKey(Interview, related_name='decisions', on_delete=models.CASCADE)
    member = models.ForeignKey(BoardMember, related_name='decisions', on_delete=models.CASCADE)
    passed = models.BooleanField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Decision for {self.interview} by {self.member}'
