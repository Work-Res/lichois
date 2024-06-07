import logging

from datetime import date
from sys import stdout

from app.api.common.web import APIResponse, APIMessage
from app.api import NewApplicationDTO
from app.identifiers import WorkResidentPermitIdentifier
from app.utils import ApplicationProcesses, ApplicationStatuses
from app.api.serializers import ApplicationVersionSerializer

from app.models import ApplicationDocument, ApplicationUser, ApplicationStatus, Application, ApplicationVersion


class CreateNewApplicationService(object):
    """Responsible for creating new application records based on given process name.

        Attributes:
            new_application (ApplicationUser): user applying for visa or resident permit e.t.c
    """

    def __init__(self, new_application: NewApplicationDTO):
        self.logger = logging.getLogger(__name__)
        self.application = new_application
        self.application_document = ApplicationDocument()
        self.response = APIResponse()

    def create(self):
        """
         Create new application records.
        """
        application_identifier = self.application.applicant_identifier
        status = ['new', 'draft', 'verification', 'vetting', 'committee_evaluation']
        exits = Application.objects.filter(
            application_status__code__in=status,
            application_document__applicant__user_identifier=application_identifier)
        if exits.exists():
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"An application with (NEW) status exists for applicant: {application_identifier}, complete the "
                f"existing before open new application"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())
            print("Record already exists.")
            return None  # Avoid continuing

        application_status = self.get_application_status()
        print("application_status: ", application_status)

        if self.create_application_document():
            application = Application()
            application.application_document = self.application_document
            application.application_status = application_status
            application.process_name = self.application.proces_name
            application.application_type = self.application.proces_name
            application.last_application_version_id = 1
            application.save()

            application_version = ApplicationVersion()
            application_version.application = application
            application_version.version_number = 1
            application_version.save()
            serializer = ApplicationVersionSerializer(application_version)
            self.response.data = serializer.data
            return application_version

    def get_application_status(self):
        """
        Get existing application status for a particular process.
        """
        try:
            application_status = ApplicationStatus.objects.get(
                code__iexact=ApplicationStatuses.NEW.value
                # processes__icontains=self.application.proces_name,
                # valid_from__lt=date.today() Fixme: Correct filtering
            )
            return application_status
        except ApplicationStatus.DoesNotExist:
            error_message = (
                f"Application status ({self.application.status}) does not exist "
                f"for process name {self.application.proces_name}. "
                f"User identifier: {self.application.applicant_identifier}"
            )
            self.logger.error(error_message)
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"The system failed to create application, failed to obtain application status with "
                        f"status: {self.application.status} and for process name: {self.application.proces_name}."
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())
            
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
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"Application processes misconfigured. "
                        f"{self.application.proces_name} does not match {ApplicationProcesses.WORK_RESIDENT_PERMIT.value}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

    def get_or_create_application_user(self):
        """
        Based on given user_identifier create new application user or get existing user
        """
        try:
            user, created = ApplicationUser.objects.get_or_create(
                user_identifier=self.application.applicant_identifier,
                defaults={
                    "work_location_code": self.application.work_place,  "dob": self.application.dob,
                    "user_identifier": self.application.applicant_identifier, "full_name": self.application.full_name
                }
            )
            if created:
                self.logger.info("Created a new application user - %s", self.application.applicant_identifier)
            else:
                self.logger.info("Retrieved existing application user - %s", self.application.applicant_identifier)
            return user
        except Exception as e:
            self.logger.exception("Failed to get or create application user - %s. ERROR: %s",
                                  self.application.applicant_identifier, e)
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"The system failed to create application, failed to obtain application user with "
                        f"user identifier: {self.application.applicant_identifier}. Error, {e}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

    def create_application_document(self):
        """
         1. generate the document number for the particular process.
         2. create ApplicantUser or obtain the existing user.
        Args:
            process_name (str): the name of the process e.g resident permit.
        """
        document_number = self.generate_document()
        applicant = self.get_or_create_application_user()

        if document_number is None or applicant is None:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"The system failed to create application document, documber number: {document_number}, applicant: {applicant}. "
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())
        else:
            self.application_document.document_number = document_number
            self.application_document.applicant = applicant
            self.application_document.document_date = date.today()
            self.application_document.signed_date = date.today()
            self.application_document.save()
            api_message = APIMessage(
                code=200,
                message="Success",
                details=f"The application has been created with document number:  {document_number}."
            )
            self.response.status = True
            self.response.messages.append(api_message.to_dict())
            return self.application_document
