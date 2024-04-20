from django.db import models

from app.models import ApplicationBaseModel
from .application_document_type import AttachmentDocumentType


class ApplicationAttachment(ApplicationBaseModel):

    filename = models.CharField(max_length=200)

    storage_object_key = models.CharField(max_length=300)

    description = models.CharField(max_length=400)

    document_url = models.CharField(max_length=150)

    received_date = models.DateTimeField()

    document_type = models.ForeignKey(AttachmentDocumentType, on_delete=models.CASCADE)
