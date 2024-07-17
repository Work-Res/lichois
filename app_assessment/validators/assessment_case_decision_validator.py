import logging

from app.api.common.web import APIResponse, APIMessage
from app_assessment.api.dto import AssessmentCaseDecisionDTO
from app_assessment.models import AssessmentCaseDecision


class AssessmentCaseDecisionValidator:
    logger = logging.getLogger(__name__)

    def __init__(self, assessment_case_decision: AssessmentCaseDecisionDTO = None):
        self.assessment_case_decision = assessment_case_decision
        self.response = APIResponse()

    def check_if_decision_taken(self):
        try:
            AssessmentCaseDecision.objects.get(
                decision__in=[self.assessment_case_decision.decision],
                parent_object_id=self.assessment_case_decision.parent_object_id,
                parent_object_type=self.assessment_case_decision.parent_object_type,
                document_number=self.assessment_case_decision.note_request_dto.document_number
            )
            api_message = APIMessage(
                code=400,
                message="The decision has been taken already.",
                details=f"The decision has been taken already "
                        f"for {self.assessment_case_decision.note_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
        except AssessmentCaseDecision.DoesNotExist:
            self.logger.error("Ready for creating or updating decision")

    def check_if_update_allowable(self):
        try:
            AssessmentCaseDecision.objects.get(
                decision__in=['draft', 'pending', 'deferred'],
                parent_object_id=self.assessment_case_decision.parent_object_id,
                parent_object_type=self.assessment_case_decision.parent_object_type,
                document_number=self.assessment_case_decision.note_request_dto.document_number
            )
        except AssessmentCaseDecision.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message="The decision cannot be changed when is already recommended.",
                details=f"The decision cannot be changed when is already recommended "
                        f"for {self.assessment_case_decision.note_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.error("Ready for creating or updating decision")

    def is_valid_for_update(self):
        self.check_if_update_allowable()
        return True if len(self.response.messages) == 0 else False

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.check_if_decision_taken()
        return True if len(self.response.messages) == 0 else False
