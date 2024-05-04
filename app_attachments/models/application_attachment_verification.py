from django.db import models
from django.contrib.auth.models import User
from app_comments.models import Comment
from app.models import ApplicationBaseModel

from ..choices import VERIFICATION_STATUS
from ..models import ApplicationAttachment


class ApplicationAttachmentVerification(ApplicationBaseModel):
    document = models.ForeignKey(ApplicationAttachment, on_delete=models.CASCADE)
    verification_status = models.CharField(max_length=120, choices=VERIFICATION_STATUS)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Officer..
    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.document.name} by {self.verifier.name}"
