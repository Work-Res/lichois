import logging
from datetime import datetime

from django.db import transaction
from rest_framework.response import Response

from app.api.common.web import APIMessage, APIResponse
from app.models import Application
from app_decision.models import ApplicationDecisionType
from app.api.dto.request_dto import RequestDTO


class BaseDecisionService:
    def __init__(self, request: RequestDTO, user=None):
        self.request = request
        self.user = user
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()
        self.decision = None

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
    def update_application(self):
        application_decision_type = self.get_application_decision_type()
        if application_decision_type:
            Application.objects.filter(
                application_document__document_number=self.request.document_number
            ).update(security_clearance=application_decision_type.code)
        else:
            api_message = APIMessage(
                code=400,
                message="Application decision provided is invalid.",
                details="System failed to obtain decision type provided, check if application decision defaults."
                "records are created.",
            )
            raise Exception(api_message.to_dict())

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
