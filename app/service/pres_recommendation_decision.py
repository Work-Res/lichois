from django.db import transaction

from datetime import datetime

from app.utils.system_enums import ApplicationStatusEnum

from ..api.common.web import APIMessage

from ..api.dto import PresRecommendationRequestDTO
from ..api.serializers import PresRecommendationDecisionSerializer

from ..models import PresRecommendationDecision
from ..service import BaseDecisionService
from ..workflow import PresRecommendationDecisionTransactionData


class PresRecommendationDecisionService(BaseDecisionService):
    def __init__(self, decision_request: PresRecommendationRequestDTO):
        workflow = PresRecommendationDecisionTransactionData(
            recommendation_decision=decision_request.status.upper(),
            role=decision_request.role.upper()
        )
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.RECOMMENDATION.value,
            application_field_key="recommendation",
        )

    def create_pres_recommendation_decision(self):
        return self.create_decision(PresRecommendationDecision, PresRecommendationDecisionSerializer)

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
                role=self.request.role
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
            print("self.response.result(): ", self.response.result())
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
                document_number=self.request.document_number,
                role=self.request.role
            )
            api_message = APIMessage(
                code=200,
                message="President Recommendation Decision retrieved successfully.",
                details="President Recmmendation retrieved successfully.",
            )
            self.response.status = "success"
            self.response.data = serializer_class(self.decision).data
            print("self.response.data: ", self.response.data)
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
