

import logging

from app.api.common.web import APIResponse, APIMessage
from app_assessment.api.dto import AssessmentNoteRequestDTO
from app_assessment.models import AssessmentCaseDecision, AssessmentCaseSummary, AssessmentCaseNote


class AssessmentNoteValidator:
    logger = logging.getLogger(__name__)

    def __init__(self, assessment_note_request_dto: AssessmentNoteRequestDTO = None):
        self.assessment_note_request_dto = assessment_note_request_dto
        self.response = APIResponse()

    def check_if_exists_already(self):
        try:
            AssessmentCaseNote.objects.get(
                parent_object_id=self.assessment_case_decision.parent_object_id,
                parent_object_type=self.assessment_case_decision.parent_object_type,
                document_number=self.assessment_case_decision.note_request_dto.document_number,
                note_type=None
            )
            api_message = APIMessage(
                code=400,
                message="The case note has been created already.",
                details=f"The case summary has been created already "
                        f"for {self.assessment_case_decision.note_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
        except AssessmentCaseDecision.DoesNotExist:
            self.logger.error("Ready for creating or updating decision")

    def check_if_update_allowable(self):
        try:
            assessment_summary = AssessmentCaseSummary.objects.get(
                parent_object_id=self.assessment_case_decision.parent_object_id,
                parent_object_type=self.assessment_case_decision.parent_object_type,
                document_number=self.assessment_case_decision.note_request_dto.document_number
            )
            assessment_decision = AssessmentCaseDecision.objects.filter(
                parent_object_id=assessment_summary.id,
                parent_object_type=assessment_summary.get_parent_object_type(),
                decision__in=['draft', 'pending']
            )
            if not assessment_decision.exists():
                api_message = APIMessage(
                    code=400,
                    message="The case summary cannot be edited.",
                    details=f"The case summary cannot be edited for"
                            f"for {self.assessment_case_decision.note_request_dto.document_number}, summary is in ["
                            f"DEFERRED OR RECOMMENDED]."
                )
                self.response.messages.append(api_message.to_dict())
        except AssessmentCaseDecision.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message="The case summary not found.",
                details=f"The case summary not found"
                        f"for {self.assessment_case_decision.note_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.error("The case summary not found.")

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.check_if_exists_already()
        return True if len(self.response.messages) == 0 else False

    def is_valid_to_update(self):
        self.check_if_update_allowable()
        return True if len(self.response.messages) == 0 else False
