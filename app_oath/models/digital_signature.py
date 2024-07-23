from django.db import models

from app_oath.models.oath_document import OathDocument
from authentication.models import User


class DigitalSignature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signature = models.ImageField(upload_to='signatures/')
    created_at = models.DateTimeField(auto_now_add=True)
    oath_document = models.ForeignKey(OathDocument, on_delete=models.CASCADE)

    class Meta:
        app_label = 'app_oath'
        db_table = 'app_oath_digital_signature'
