from django.db import models

from .application_document import ApplicationDocument
from .application_status import ApplicationStatus

from base_module.model_mixins import BaseUuidModel

from ..utils import ApplicationDecisionEnum


class Application(BaseUuidModel):
    """
    Model representing a work permit application.

    Attributes:
        user (ForeignKey): The user who created or owns the document.
        application_document (Foreign): Document for applicant.
        application_status (Foreign): The status for the application.
    """

    last_application_version_id = models.IntegerField()
    application_document = models.ForeignKey(
        ApplicationDocument, on_delete=models.CASCADE
    )
    process_name = models.CharField(max_length=200, null=False, blank=False)
    application_status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=200)
    batched = models.BooleanField(null=True, blank=True, default=False)
    permit_period = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    verification = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    recommendation = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    security_clearance = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    assessment = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    board = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    submission_date = models.DateField(auto_now=True)

    def full_name(self):
        return self.application_document.applicant.full_name

    def __str__(self):
        return f"Application {self.application_document.document_number}"

    class Meta:
        verbose_name_plural = "Applications"
        ordering = ["-created"]
