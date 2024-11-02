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

    supporting_documents = models.URLField(blank=True, null=True)

    contract_letter = models.URLField(blank=True, null=True)

    work_application_letter = models.URLField(blank=True, null=True)

    employer_justification = models.URLField(blank=True, null=True)

    reference_proof = models.URLField(blank=True, null=True)

    passport_photo_1 = models.URLField(blank=True, null=True)

    passport_photo_2 = models.URLField(blank=True, null=True)

    certificate_of_incorporation = models.URLField(blank=True, null=True)

    bank_statement_1 = models.URLField(blank=True, null=True)

    bank_statement_2 = models.URLField(blank=True, null=True)

    bank_statement_3 = models.URLField(blank=True, null=True)

    investment_proof = models.URLField(blank=True, null=True)

    description = models.CharField(max_length=400)

    document_url = models.CharField(max_length=150)

    received_date = models.DateTimeField()

    document_type = models.ForeignKey(AttachmentDocumentType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Application Attachments"
        ordering = ['-created']
