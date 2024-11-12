import logging

from django.db.utils import IntegrityError
from django.db import transaction

from app.api.common.web import APIResponse, APIMessage
from app.utils import ApplicationStatusEnum

from workresidentpermit.classes.service import (
    WorkResidentPermitReplacementHistoryService,
)

from ..api import NewApplicationDTO
from ..api.dto import ReplacementApplicationDTO

from app.models import (
    ApplicationDocument,
    Application,
    ApplicationVersion,
    ApplicationReplacement,
)
from app_comments.models import Comment
from ..exceptions.application_renewal_exception import ApplicationReplacementException


class ReplacementApplicationService(object):
    """Responsible for creation of an application renewal,  records based on given process name.

    Attributes:
        replacement_application_dto: ReplacementApplicationDTO
    """

    def __init__(self, replacement_application_dto: ReplacementApplicationDTO):
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()
        self.replacement_application_dto = replacement_application_dto
        self.new_replacement_application = None
        self.previous_application = self.get_previous_application()
        self.new_application_version = None
        self.application_document = ApplicationDocument()

    def get_previous_application(self) -> None:
        """
        Retrieve the previous accepted application based on the renewal application's document number.
        """
        try:
            previous_application = Application.objects.get(
                application_document__document_number=self.replacement_application_dto.document_number,
                application_status__code__iexact=ApplicationStatusEnum.ACCEPTED.value,
            )
            return previous_application
        except Application.DoesNotExist:
            error_message = (
                f"An application with status '{ApplicationStatusEnum.ACCEPTED.value}' does not exist for creating "
                f"renewal: {self.replacement_application_dto.document_number}."
            )
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"Previous application not found, replacement creation aborted - "
                f"{self.replacement_application_dto.document_number}.",
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.error(error_message)
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred during renewal creation: {str(e)}"
            )
        else:
            return previous_application

    @transaction.atomic()
    def create_application_replacement(
        self,
        new_application_version: ApplicationVersion = None,
        comment: Comment = None,
        submitted_by=None,
    ):

        if not new_application_version:
            self.logger.error(
                "New application version is required to create a replacement."
            )
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=f"New application version is required to create a renewal for "
                f"{self.self.appeal_application_dto.document_number}",
            )
            self.response.messages.append(api_message.to_dict())
            return

        try:
            self.new_replacement_application = ApplicationReplacement.objects.create(
                previous_application=self.previous_application,
                replacement_application=new_application_version.application,
                comment=comment,
                submitted_by=submitted_by,
            )
        except IntegrityError as e:
            self.logger.error(
                "An integrity error occurred while creating the application renewal."
            )
            details = f"Failed to create new renewal application for {self.replacement_application_dto.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details,
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationReplacementException(detail=details)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            details = f"Failed to create new renewal application for {self.replacement_application_dto.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details,
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationReplacementException(detail=details)

    def create_all(self, new_application_version: ApplicationVersion = None):

        self.logger.info(
            "Starting create_all method with new_application_version: %s",
            new_application_version.application.application_document.document_number,
        )

        try:
            self.logger.info("Creating application renewal.")
            self.create_application_replacement(
                new_application_version=new_application_version
            )
            self.logger.info(
                "Successfully created replacement application with document_number: %s",
                self.replacement_application_dto.document_number,
            )

            self.logger.info("Creating replacement application history.")
            WorkResidentPermitReplacementHistoryService(
                document_number=self.replacement_application_dto.document_number,
                application_type=self.replacement_application_dto.proces_name,
                application_user=self.previous_application.application_document.applicant,
                process_name=self.previous_application.process_name,
            ).create_application_replacement_history()
            self.logger.info("Successfully created replacement application history.")

        except Exception as e:
            self.logger.error("Error occurred during create_all method: %s", str(e))
            raise

    def prepare_new_application_dto(self) -> NewApplicationDTO:
        """
        Prepare the DTO for the new application based on the previous application data.
        """
        new_application_dto = NewApplicationDTO(
            process_name=self.replacement_application_dto.proces_name,
            applicant_identifier=self.replacement_application_dto.applicant_identifier,
            status=ApplicationStatusEnum.NEW.value,
        )
        new_application_dto.dob = (
            self.previous_application.application_document.applicant.dob
        )
        new_application_dto.full_name = (
            self.previous_application.application_document.applicant.full_name
        )
        new_application_dto.application_type = (
            self.previous_application.application_type
        )
        new_application_dto.work_place = self.replacement_application_dto.work_place
        return new_application_dto