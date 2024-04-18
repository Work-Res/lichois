from django.db import models

from app.models.application_version import ApplicationVersion
from .application_document_type import AttachmentDocumentType

from base_module.model_mixins import BaseUuidModel


class ApplicationAttachment(BaseUuidModel):

    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)

    filename = models.CharField(max_length=200)

    storage_object_key = models.CharField(max_length=300)

    description = models.CharField(max_length=400)

    document_url = models.CharField(max_length=150)

    received_date = models.DateTimeField()

    document_type = models.ForeignKey(AttachmentDocumentType, on_delete=models.CASCADE)
