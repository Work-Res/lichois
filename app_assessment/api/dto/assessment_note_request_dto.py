

class AssessmentNoteRequestDTO:

    def __init__(self, document_number, parent_object_id=None, parent_object_type=None, note_text=None, note_type=None):
        self.document_number = document_number
        self.parent_object_id = parent_object_id
        self.parent_object_type = parent_object_type
        self.note_text = note_text
        self.note_type = note_type