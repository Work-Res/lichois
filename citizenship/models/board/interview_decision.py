from django.db import models

from citizenship.models.board import Interview, Member


class InterviewDecision(models.Model):
    interview = models.ForeignKey(Interview, related_name='decisions', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='decisions', on_delete=models.CASCADE)
    passed = models.BooleanField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Decision for {self.interview} by {self.member}'
