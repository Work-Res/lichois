from django.db import models

from app.models import ApplicationBaseModel
from authentication.models import User


class OathDocument(ApplicationBaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'app_oath'
        db_table = 'app_oath_oath_document'
