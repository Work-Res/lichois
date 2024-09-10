from django.db import models
from authentication.models import User

# from app.models import ApplicationBaseModel

from base_module.model_mixins import BaseUuidModel


class Comment(BaseUuidModel):

    document_number = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField()
    comment_type = models.CharField(max_length=50)

    def __str__(self):
        return self.comment_text
