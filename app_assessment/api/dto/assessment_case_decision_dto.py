from app_assessment.api.dto import AssessmentNoteRequestDTO


class AssessmentCaseDecisionDTO:

    def __init__(self, note_request_dto: AssessmentNoteRequestDTO, parent_object_id=None, parent_object_type=None,
                 author=None,
                 author_role=None,
                 decision=None
                 ):
        self.note_request_dto = note_request_dto
        self.parent_object_id = parent_object_id
        self.parent_object_type = parent_object_type
        self.author = author
        self.author_role = author_role
        self.decision = decision
