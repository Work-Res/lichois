import logging

from datetime import date

from app.api.common.web import APIResponse, APIError
from app.identifiers import WorkResidentPermitIdentifier
from app.utils import ApplicationProcesses

from app.models import ApplicationDocument, ApplicationUser, ApplicationStatus, Application, ApplicationVersion
from django.db import transaction


class CreateNewApplication(object):
    """Responsible for creating new application records based on given process name.

        Attributes:
            new_application (ApplicationUser): user applying for visa or resident permit e.t.c
    """

    def __init__(self, new_application):
        self.logger = logging.getLogger(__name__)
        self.application = new_application
        self.application_document = ApplicationDocument()
        self.response = APIResponse()

    def create(self):
        """
         Create new application records.
        """
        application_status = self.get_application_status()
        application_document = self.create_application_document()

        application = Application()
        application.application_document = application_document
        application.application_status = application_status
        application.last_application_version_id = 1
        application.save()

        application_version = ApplicationVersion()
        application_version.application = application
        application_version.version_number = 1
        application_version.save()
        return application_version

    def get_application_status(self):
        """
        Get existing application status for a particular process.
        """
        try:
            application_status = ApplicationStatus.objects.get(
                code=self.application.status,
                # processes__icontains=self.application.proces_name,
                valid_from__lt=date.today()
            )
            return application_status
        except ApplicationStatus.DoesNotExist:
            error_message = (
                f"Application status ({self.application.status}) does not exist "
                f"for process name {self.application.proces_name}. "
                f"User identifier: {self.application.applicant_identifier}"
            )
            self.logger.error(error_message)
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system failed to create application, failed to obtain application status with "
                        f"status: {self.application.status} and for process name: {self.application.proces_name}."
            )
            self.response.messages.append(api_message)
            
    def generate_document(self):
        """
        Generate document based on given process.
        """
        if self.application.proces_name == ApplicationProcesses.WORK_RESIDENT_PERMIT.value:
            work_identifier = WorkResidentPermitIdentifier(
                address_code=self.application.work_place, dob=self.application.dob)
            return work_identifier.identifier
        else:
            self.logger.debug(" application process: %s does not match to any configured application "
                              "processes. ", self.application.proces_name)
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system failed to create application, failed to obtain application user with "
                        f"user identifier: {self.application.applicant_identifier}."
            )
            self.response.messages.append(api_message)

    def get_or_create_application_user(self):
        """
        Based on given user_identifier create new application user or get existing user
        """
        try:
            with transaction.atomic():
                user, created = ApplicationUser.objects.get_or_create(
                    user_identifier=self.application.applicant_identifier
                )
                if created:
                    self.logger.info("Created a new application user - %s", self.application.applicant_identifier)
                else:
                    self.logger.info("Retrieved existing application user - %s", self.application.applicant_identifier)
                return user
        except Exception as e:
            self.logger.exception("Failed to get or create application user - %s. ERROR: %s",
                                  self.application.applicant_identifier, e)
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system failed to create application, failed to obtain application user with "
                        f"user identifier: {self.application.applicant_identifier}."
            )
            self.response.messages.append(api_message)

    def create_application_document(self):
        """
         1. generate the document number for the particular process.
         2. create ApplicantUser or obtain the existing user.
        Args:
            process_name (str): the name of the process e.g resident permit.
        """
        self.application_document.document_number = self.generate_document()
        self.application_document.applicant = self.get_or_create_application_user()
        self.application_document.document_date = date.today()
        self.application_document.signed_date = date.today()
        self.application_document.save()
        return self.application_document
