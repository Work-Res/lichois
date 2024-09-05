from django.db import transaction
from datetime import datetime

from app.api.common.web import APIMessage
from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import (
    RecommendationDecisionTransactionData,
)
from citizenship.api.dto import RecommendationDecisionRequestDTO

from citizenship.api.serializers import RecommendationDecisionSerializer
from citizenship.models import RecommendationDecision


class RecommendationDecisionService(BaseDecisionService):
    def __init__(self, decision_request: RecommendationDecisionRequestDTO):
        workflow = RecommendationDecisionTransactionData(
            recommendation_decision=decision_request.status.upper()
        )
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.RECOMMENDATION.value,
            application_field_key="recommendation",
        )
        self.request = decision_request

    def create_recommendation(self):
        return self.create_decision(
            RecommendationDecision, RecommendationDecisionSerializer
        )

    def retrieve_recommendation(self):
        return self.retrieve_decision(
            RecommendationDecision, RecommendationDecisionSerializer
        )

    def _security_clearance(self):
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
            self.logger.info(
                f"CITIZENSHIP GOT CREATE DECISION: {application_decision_type}"
            )
            if application_decision_type is None:
                return self.response

            self.decision = decision_model.objects.create(
                status=application_decision_type,
                document_number=self.request.document_number,
                approved_by=self.request.user,
                date_approved=datetime.now(),
                role=self.request.role,
            )

            self.logger.info(
                f"Citizenship Application for model {decision_model} {self.request.document_number} decision created successfully."
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
            self._deactivate_current_task()
            self._activate_next_task()

        return self.response.result()
