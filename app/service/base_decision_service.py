import logging
from datetime import datetime

from django.db import transaction
from rest_framework.response import Response

from app_comments.models import Comment
from app_decision.models import ApplicationDecisionType
from workflow.classes.task_deactivation import TaskDeActivation
from workflow.signals import create_or_update_task_signal

from ..api.common.web import APIMessage, APIResponse
from ..api.dto.request_dto import RequestDTO
from ..classes.mixins.update_application_mixin import UpdateApplicationMixin
from ..models import Application


class BaseDecisionService(UpdateApplicationMixin):
    def __init__(
        self,
        request: RequestDTO,
        user=None,
        application_field_key=None,
        task_to_deactivate=None,
        workflow=None,
    ):
        self.request = request
        self.user = user
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()
        self.decision = None
        self.application_field_key = application_field_key
        self.application = self._get_application()
        self.workflow = workflow
        self.task_to_deactivate = task_to_deactivate

    def get_application_decision_type(self):
        try:
            application_decision_type = ApplicationDecisionType.objects.get(
                code__iexact=self.request.status
            )
            return application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message=f"Application decision provided is invalid: {self.request.status}.",
                details="System failed to obtain decision type provided, check if application decision defaults."
                "records are created.",
            )
            self.response.messages.append(api_message.to_dict())
            return None

    @transaction.atomic
    def create_decision(self, decision_model, serializer_class):
        application_decision_type = self.get_application_decision_type()
        if application_decision_type is None:
            return self.response

        self.decision = decision_model.objects.create(
            status=application_decision_type,
            summary=self.request.summary,
            document_number=self.request.document_number,
            approved_by=self.user,
            date_approved=datetime.now(),
        )

        api_message = APIMessage(
            code=200,
            message="Decision created successfully.",
            details="Decision created successfully.",
        )
        self.response.status = "success"
        self.response.data = serializer_class(self.decision).data
        self.response.messages.append(api_message.to_dict())

        self.update_application_field(
            self.request.document_number,
            self.application_field_key,
            application_decision_type.code,
        )
        self._create_comment()
        self._deactivate_current_task()
        self._activate_next_task()

        return Response(self.response.result())

    def retrieve_decision(self, decision_model, serializer_class):
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
        return Response(self.response.result())

    def _get_application(self):
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
        if self.task_to_deactivate:
            task_deactivation = TaskDeActivation(
                application=self.application,
                source=None,
                model=None,
            )
            task_deactivation.update_task_by_activity(name=self.task_to_deactivate)

    def _activate_next_task(self):
        if self.workflow and self.decision:
            create_or_update_task_signal.send_robust(
                sender=self.application,
                source=self.workflow,
                application=self.application,
            )

    def _create_comment(self):
        if self.request.comment:
            return Comment.objects.create(
                user=self.user,
                comment_text=self.request.comment,
                comment_type="OVERALL_APPLICATION_COMMENT",
            )
