from django.db import models
from authentication.models import User
from app.models import ApplicationBaseModel


class Comment(ApplicationBaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField()
    comment_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.comment_type}"
