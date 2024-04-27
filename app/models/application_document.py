from django.db import models

from .application_user import ApplicationUser

from base_module.model_mixins import BaseUuidModel


class ApplicationDocument(BaseUuidModel):
    """
    Model representing a document, contains application generated document number, contains applicant.

    Attributes:
        applicant (ForeignKey): User who has submitted the application.
        document_number (str): The number assigned to the document, it is system generated identifier for the application.
        document_date (date): The date of the document.
        signed_date (date): The date when the document was signed.
        submission_customer (str): The customer associated with the document submission.
    """
    applicant = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, null=False, blank=False)
    document_number = models.CharField(max_length=100, null=False, blank=False)
    document_date = models.DateField(null=False, blank=False)
    signed_date = models.DateField()
    submission_customer = models.CharField(max_length=250)

    def __str__(self):
        return f"Document {self.document_number}"

    class Meta:
        verbose_name_plural = "ApplicationDocuments"
