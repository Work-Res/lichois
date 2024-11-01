from django.db import models

from app.models import ApplicationBaseModel
from .application_document_type import AttachmentDocumentType


class ApplicationAttachment(ApplicationBaseModel):

    filename = models.CharField(max_length=200)

    filenumber = models.IntegerField()

    storage_object_key = models.CharField(max_length=300)

    certified_passport = models.URLField(blank=True, null=True)

    educational_certificates = models.URLField(blank=True, null=True)

    advertisement_proof = models.URLField(blank=True, null=True)

    curriculum_vitae = models.URLField(blank=True, null=True)

    supporting_documents_url = models.URLField(blank=True, null=True)

    contract_letter = models.URLField(blank=True, null=True)

    work_application_letter = models.URLField(blank=True, null=True)

    employeer_justification = models.URLField(blank=True, null=True)

    relevant_experience = models.URLField(blank=True, null=True)

    description = models.CharField(max_length=400)

    document_url = models.CharField(max_length=150)

    received_date = models.DateTimeField()

    document_type = models.ForeignKey(AttachmentDocumentType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Application Attachments"
        ordering = ['-created']
