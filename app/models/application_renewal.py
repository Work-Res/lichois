from django.db import models

from app_comments.models import Comment
from .application import Application

from base_module.model_mixins import BaseUuidModel


class ApplicationRenewal(BaseUuidModel):

    previous_application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, related_name='previous_application')
    renewal_application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, related_name='renewal_application')
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    submitted_by = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.decision}'

    class Meta:
        app_label = 'app'
