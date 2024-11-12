from django.db import models

from app_comments.models import Comment
from .application import Application

from base_module.model_mixins import BaseUuidModel


class ApplicationAppeal(BaseUuidModel):
    previous_application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appealed_applications'
    )
    appeal_application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appeal_applications'
    )
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    submitted_by = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.previous_application} - {self.appeal_application}'

    class Meta:
        app_label = 'app'
