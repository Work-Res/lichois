import logging

from app.service.base_decision_service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import AssessmentCaseDecisionTransactionData
from app_assessment.api.dto import AssessmentCaseDecisionDTO
from django.db import transaction, IntegrityError

from app_assessment.api.serializers import AssessmentCaseDecisionSerializer
from app_assessment.models import AssessmentCaseDecision

from app.api.common.web import APIResponse, APIMessage


class AssessmentCaseDecisionService(BaseDecisionService):

    def __init__(self, assessment_case_decision_dto: AssessmentCaseDecisionDTO = None):
        self.assessment_case_decision_dto = assessment_case_decision_dto
        self.response = APIResponse()
        self.logger = logging.getLogger(__name__)

        workflow = AssessmentCaseDecisionTransactionData()
        workflow.assessment_decision = "ACCEPTED"

        super().__init__(
            request=assessment_case_decision_dto,
            application_field_key="assessment",
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.ASSESSMENT.value,
        )

    def create_assessment(self):
        return self.create_decision(
            AssessmentCaseDecision, AssessmentCaseDecisionSerializer
        )

    def retrieve_assessment(self):
        return self.retrieve_decision(
            AssessmentCaseDecision, AssessmentCaseDecisionSerializer
        )

    def create(self):
        self.logger.info(
            f"Creating a case note for {self.assessment_case_decision_dto.document_number}"
        )
        try:
            with transaction.atomic():

                case_case_decision = AssessmentCaseDecision.objects.get(
                    document_number=self.assessment_case_decision_dto.document_number
                )
                if case_case_decision:
                    self.logger.error(
                        f"Assessment case decision with document number  "
                        f"{self.assessment_case_decision_dto.document_number} already exists."
                    )
                    api_message = APIMessage(
                        code=400,
                        message="Assessment summary decision already exists.",
                        details="Assessment summary decision already exists.",
                    )
                    self.response.status = False
                    self.response.messages.append(api_message.to_dict())
                    return
                data = AssessmentCaseDecision.objects.create(
                    parent_object_id=self.assessment_case_decision_dto.parent_object_id,
                    parent_object_type=self.assessment_case_decision_dto.parent_object_type,
                    author=self.assessment_case_decision_dto.author,
                    author_role=self.assessment_case_decision_dto.author_role,
                    decision=self.assessment_case_decision_dto.decision,
                    document_number=self.assessment_case_decision_dto.document_number,
                )
                api_message = APIMessage(
                    code=200,
                    message="Assessment summary decision has been created.",
                    details="Assessment summary decision has been created.",
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
                self.response.data = AssessmentCaseDecisionSerializer(data).data
                self.logger.info(
                    f"Created a summary decision for {self.assessment_case_decision_dto.document_number}"
                )
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")

    def update(self):
        self.logger.info(
            f"Updating a summary decision for {self.assessment_case_decision_dto.document_number}"
        )
        try:
            with transaction.atomic():
                # Fetch the existing case decision
                case_case_decision = AssessmentCaseDecision.objects.get(
                    document_number=self.assessment_case_decision_dto.document_number,
                    parent_object_id=self.assessment_case_decision_dto.parent_object_id,
                    parent_object_type=self.assessment_case_decision_dto.parent_object_type,
                )
                self.logger.debug(
                    f"Fetched case decision for {self.assessment_case_decision_dto.document_number}"
                )

                updated_data = self.assessment_case_decision_dto.__dict__
                for key, value in updated_data.items():
                    setattr(case_case_decision, key, value)
                case_case_decision.save()
                self.logger.info(
                    f"Updated case decision for {self.assessment_case_decision_dto.document_number}"
                )
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been updated.",
                    details="Assessment note has been updated.",
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except AssessmentCaseDecision.DoesNotExist:
            self.logger.error(
                f"Assessment case decision with document number  "
                f"{self.assessment_case_decision_dto.document_number} does not exist."
            )

        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")
