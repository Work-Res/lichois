from django.db import models

from app.models import ApplicationBaseModel
from app_comments.models import Comment


class AssessmentResult(ApplicationBaseModel):

    score = models.IntegerField()
    output_results = models.JSONField()
    result_date = models.DateField()
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
