from django.db import models

from app.models import ApplicationBaseModel
from .application_document_type import AttachmentDocumentType


class ApplicationAttachment(ApplicationBaseModel):

    filename = models.CharField(max_length=200)

    filenumber = models.IntegerField()

    storage_object_key = models.CharField(max_length=300)

    certified_passport_copy = models.URLField()

    passport_photo_1 = models.URLField()

    passport_photo_2 = models.URLField()

    description = models.CharField(max_length=400)

    document_url = models.CharField(max_length=150)

    received_date = models.DateTimeField()

    document_type = models.ForeignKey(AttachmentDocumentType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Application Attachments"
        ordering = ['-created']
