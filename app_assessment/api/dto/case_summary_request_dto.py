

class CaseSummaryRequestDTO:

    def __init__(self, document_number: str = None, parent_object_id=None, parent_type=None, data=None):
        self.document_number = document_number
        self.parent_object_id = parent_object_id
        self.parent_type = parent_type
        self.data = data
