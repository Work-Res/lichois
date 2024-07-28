

import logging

from app.api.common.web import APIResponse, APIMessage
from app_assessment.api.dto import AssessmentNoteRequestDTO
from app_assessment.models import AssessmentCaseDecision, AssessmentCaseSummary, AssessmentCaseNote


class AssessmentNoteValidator:
    logger = logging.getLogger(__name__)

    def __init__(self, assessment_note_request_dto: AssessmentNoteRequestDTO = None):
        self.assessment_note_request_dto = assessment_note_request_dto
        self.response = APIResponse()

    def check_if_exists_case_summary_exists(self):
        try:
            AssessmentCaseSummary.objects.get(
                document_number=self.assessment_note_request_dto.document_number
            )
        except AssessmentCaseDecision.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message="The case summary must exists in order to create a note for it.",
                details=f"The case summary must exists in order to create a note for it, "
                        f"for {self.assessment_note_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.warning("Failed to create note for case summary. ")

    def check_if_update_allowable(self):
        try:
            AssessmentCaseSummary.objects.get(
                document_number=self.assessment_note_request_dto.document_number
            )
            notes = AssessmentCaseNote.objects.filter(
                parent_object_id=self.assessment_note_request_dto.parent_object_id,
                parent_object_type=self.assessment_note_request_dto.parent_object_type
            )
            if not notes.exists():
                raise Exception("Note not found for updating")
        except AssessmentCaseSummary.DoesNotExist:
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
        self.check_if_exists_case_summary_exists()
        return True if len(self.response.messages) == 0 else False

    def is_valid_to_update(self):
        self.check_if_update_allowable()
        return True if len(self.response.messages) == 0 else False
