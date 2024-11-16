import logging
from datetime import datetime

from django.db import transaction

from app.models.security_clearance import SecurityClearance
from app.workflow.transaction_data import BaseTransactionData
from app_comments.models import Comment
from workflow.classes.task_deactivation import TaskDeActivation
from workflow.signals import create_or_update_task_signal

from ..api.common.web import APIMessage, APIResponse
from ..api.dto.request_dto import RequestDTO
from ..classes.mixins.update_application_mixin import UpdateApplicationMixin
from ..models import Application, ApplicationDecisionType


class BaseDecisionService(UpdateApplicationMixin):
    """
    Base service class for handling application decisions.

    This class provides methods to create and retrieve decisions related to applications.
    It also handles updating application fields, deactivating current tasks, and activating next tasks in the workflow.
    """

    def __init__(
        self,
        request: RequestDTO = None,
        application_field_key=None,
        task_to_deactivate=None,
        workflow: BaseTransactionData = None,
    ):
        """
        Initialize the service with the request data, user, and other optional parameters.

        Args:
            request (RequestDTO): The request data transfer object containing the decision details.
            user: The user making the request.
            application_field_key: The key of the application field to be updated.
            task_to_deactivate: The task to be deactivated in the workflow.
            workflow: The workflow instance for task activation.
        """
        self.request = request
        self.response = APIResponse()
        self.decision = None
        self.application_field_key = application_field_key
        self.application = self._get_application()
        self.workflow = workflow
        self.task_to_deactivate = task_to_deactivate
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.security_clearance = None
        self.gazette_batch_application = None

    def get_application_decision_type(self):
        """
        Retrieve the application decision type based on the request status.

        Returns:
            ApplicationDecisionType: The application decision type object if found, otherwise None.
        """
        try:
            application_decision_type = ApplicationDecisionType.objects.get(
                code__iexact=self.request.status
            )
            return application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            self.logger.debug(f"Decision not found {self.request.status}")
            api_message = APIMessage(
                code=400,
                message=f"Application decision provided is invalid: {self.request.status}.",
                details="System failed to obtain decision type provided, check if application decision defaults."
                "records are created.",
            )
            self.response.messages.append(api_message.to_dict())
            return None

    def create_decision(self, decision_model, serializer_class):
        """
        Create a new decision record and update the application accordingly.

        Args:
            decision_model: The model class for the decision.
            serializer_class: The serializer class for the decision model.

        Returns:
            Response: The response object containing the result of the operation.
        """
        self.logger.info("STARTED: At the create_decision.")
        with transaction.atomic():
            application_decision_type = self.get_application_decision_type()
            self.logger.info(f"GOT CREATE DECISION: {application_decision_type}")
            if application_decision_type is None:
                return self.response.result()

            self.decision = decision_model.objects.create(
                status=application_decision_type,
                document_number=self.request.document_number,
                approved_by=self.request.user,
                date_approved=datetime.now(),
            )

            self.logger.info(
                f"Application for model {decision_model} {self.request.document_number} decision created successfully."
            )
            api_message = APIMessage(
                code=200,
                message="Decision created successfully.",
                details=f"Decision created successfully for the application {self.request.document_number}.",
            )
            self.response.status = "success"
            self.response.data = serializer_class(self.decision).data
            self.response.messages.append(api_message.to_dict())

            self.logger.info("END: Created a decision model.")

            # Update the application field with the decision status
            self.update_application_field(
                document_number=self.request.document_number,
                field_key=self.application_field_key,
                field_value=application_decision_type.code.upper(),
            )

            self.application.refresh_from_db()

            self._create_comment()
            # self._deactivate_current_task()
            self._activate_next_task()
        return self.response.result()

    def retrieve_decision(self, decision_model, serializer_class):
        """
        Retrieve an existing decision record based on the document number.

        Args:
            decision_model: The model class for the decision.
            serializer_class: The serializer class for the decision model.

        Returns:
            Response: The response object containing the result of the operation.
        """
        try:
            self.decision = decision_model.objects.get(
                document_number=self.request.document_number
            )
            api_message = APIMessage(
                code=200,
                message="Decision retrieved successfully.",
                details="Decision retrieved successfully.",
            )
            self.response.status = "success"
            self.response.data = serializer_class(self.decision).data
            self.response.messages.append(api_message.to_dict())
        except decision_model.DoesNotExist:
            api_message = APIMessage(
                code=404,
                message="Decision not found.",
                details="No decision found with the provided document number.",
            )
            self.response.messages.append(api_message.to_dict())
            self.response.status = "error"
        return self.response.result()

    def _get_application(self):
        """
        Retrieve the application based on the document number from the request.

        Returns:
            Application: The application object if found, otherwise None.
        """
        try:
            application = Application.objects.get(
                application_document__document_number=self.request.document_number
            )
            return application
        except Application.DoesNotExist:
            api_message = APIMessage(
                code=404,
                message="Application not found.",
                details="No application found with the provided document number.",
            )
            self.response.messages.append(api_message.to_dict())
            return None

    def _deactivate_current_task(self):
        """
        Deactivate the current task if a task to deactivate is specified.
        """

        if self.task_to_deactivate:
            task_deactivation = TaskDeActivation(
                application=self.application,
                source=None,
                model=None,
            )
            task_deactivation.update_task_by_activity(name=self.task_to_deactivate)

    def _activate_next_task(self):
        """
        Activate the next task in the workflow if a workflow and decision are specified.
        """
        try:
            if self.workflow and self.decision:
                self.logger.info(
                    f"Starting task activation for request with document_number: {self.request.document_number}"
                )

                # Log the decision and workflow details
                self.logger.info(
                    f"Workflow: {self.workflow}, Decision: {self.decision}"
                )

                # Log the start of the security clearance process
                self.logger.info("Setting security clearance.")
                self.set_security_clearance()
                self.logger.info("Security clearance set successfully.")

                # Log the task signal creation
                self.logger.info(
                    f"Creating or updating task for application: {self.application}"
                )
                create_or_update_task_signal.send_robust(
                    sender=self.application,
                    source=self.workflow,
                    application=self.application,
                )
                self.logger.info("Task signal sent successfully.")
            else:
                self.logger.warning(
                    f"Cannot activate next task. Workflow({self.workflow}) or decision{self.decision} is missing."
                )

        except Exception as e:
            self.logger.error(f"Error occurred while activating next task: {str(e)}")
            raise

    def _create_comment(self):
        """
        Create a comment if a comment/summary is provided in the request.

        Returns:
            Comment: The created comment object.
        """
        if self.request.summary:
            return Comment.objects.create(
                user=self.request.user,
                comment_text=self.request.summary,
                document_number=self.request.document_number,
                comment_type=self.request.comment_type,
            )

    def _security_clearance(self):
        try:
            return SecurityClearance.objects.get(
                document_number=self.request.document_number
            )
        except SecurityClearance.DoesNotExist:
            self.logger.info(
                f"Security clearance is pending for {self.request.document_number}"
            )
        return None

    def _has_security_clearance(self):
        return hasattr(self.workflow, "security_clearance")

    def set_security_clearance(self):
        self.security_clearance = self._security_clearance()
        if self.security_clearance:
            self.workflow.security_clearance = self.security_clearance.status.code
            self.logger.info(
                f"Security clearance set in workflow {self.workflow.current_status} for {self.request.document_number}"
            )
