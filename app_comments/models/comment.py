from django.db import models
from django.contrib.auth.models import User
from base_module.model_mixins import BaseUuidModel

from app.models.application_version import ApplicationVersion


class Comment(BaseUuidModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_type = models.CharField(max_length=50)
    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.comment_type}"
