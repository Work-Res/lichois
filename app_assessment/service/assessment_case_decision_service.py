from app_assessment.api.dto import AssessmentCaseDecisionDTO
from django.db import transaction, IntegrityError

from app_assessment.api.serializers import AssessmentCaseDecisionSerializer
from app_assessment.models import AssessmentCaseDecision

from app.api.common.web import APIResponse, APIMessage


class AssessmentCaseDecisionService:

    def __init__(self, assessment_case_decision_dto: AssessmentCaseDecisionDTO=None):
        self.assessment_case_decision_dto = assessment_case_decision_dto
        self.response = APIResponse()

    def create(self):
        self.logger.info(f"Creating a case note for {self.assessment_case_decision_dto.document_number}")
        try:
            with transaction.atomic():
                data = AssessmentCaseDecision.objects.create(
                    parent_object_id=self.assessment_case_decision_dto.parent_object_id,
                    parent_object_type=self.assessment_case_decision_dto.parent_object_type,
                    author=self.assessment_case_decision_dto.author,
                    author_role=self.assessment_case_decision_dto.author_role,
                    decision=self.assessment_case_decision_dto.decision
                )
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been created.",
                    details="Assessment note has been created."
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
                self.response.data = AssessmentCaseDecisionSerializer(data=data).data
                self.logger.info(f"Created a case note for {self.note_request_dto.document_number}")
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")

    def update(self):
        self.logger.info(f"Updating a case note for {self.note_request_dto.document_number}")
        try:
            with transaction.atomic():
                # Fetch the existing case decision
                case_case_decision = AssessmentCaseDecision.objects.get(
                    document_number=self.note_request_dto.document_number,
                    parent_object_id=self.note_request_dto.parent_object_id,
                    parent_object_type=self.note_request_dto.parent_object_type
                )
                self.logger.debug(f"Fetched case decision for {self.note_request_dto.document_number}")

                updated_data = self.assessment_case_decision_dto.__dict__
                for key, value in updated_data.items():
                    setattr(case_case_decision, key, value)
                case_case_decision.save()
                self.logger.info(f"Updated case decision for {self.note_request_dto.document_number}")
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been updated.",
                    details="Assessment note has been updated."
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except AssessmentCaseDecision.DoesNotExist:
            self.logger.error(f"Assessment case decision with document number  "
                              f"{self.note_request_dto.document_number} does not exist.")
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")
