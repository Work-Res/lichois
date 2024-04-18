from django.db import models

from .application_document import ApplicationDocument
from .application_status import ApplicationStatus

from base_module.model_mixins import BaseUuidModel


class Application(BaseUuidModel):
    """
     Model representing a work permit application.

     Attributes:
         user (ForeignKey): The user who created or owns the document.
         application_document (Foreign): Document for applicant.
         application_status (Foreign): The status for the application.
     """
    last_application_version_id = models.IntegerField()
    application_document = models.ForeignKey(ApplicationDocument, on_delete=models.CASCADE)
    application_status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Application {self.application_document.document_number}"
