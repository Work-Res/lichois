from django.db import models

from .choices import DOCUMENT_TYPES
from base_module.model_mixins import BaseUuidModel


class ProductionAttachmentDocument(BaseUuidModel):

    document_type = models.CharField(max_length=60, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=100)
    pdf_document = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.document_type} - {self.document_number}"
