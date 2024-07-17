
from app_checklist.utils import ReadJSON

from .assessment_note_service import AssessmentNoteService
from .case_summary_service import CaseSummaryService
from ..api.dto import AssessmentNoteRequestDTO, CaseSummaryRequestDTO


class AssessmentCaseService(AssessmentNoteService, CaseSummaryService):

    def __init__(self, note_request_dto: AssessmentNoteRequestDTO = None,
                 case_summary_request_dto: CaseSummaryRequestDTO = None):
        self.note_request_dto = note_request_dto
        self.case_summary_request_dto = case_summary_request_dto
        AssessmentNoteService.__init__(self, note_request_dto=note_request_dto)
        CaseSummaryService.__init__(self, case_summary_request_dto=case_summary_request_dto)

    def create_note(self):
        note_service = AssessmentNoteService(note_request_dto=self.note_request_dto)

    def create_case_summary(self):
        """Creates case summary based on submitted application forms.
        """
        CaseSummaryService.create(self)

    def read_schedules_for_decisions(self, config_location=None):
        reader = ReadJSON(file_location=self.config_location or config_location)
        schedules = reader.json_data().get("assessment_schedules")
        for key, value in schedules.items():
            pass

