

class CaseSummaryRequestDTO:

    def __init__(self, document_number: str = None, parent_object_id=None, parent_object_type=None, data=None,
                 summary=None):
        self.document_number = document_number
        self.parent_object_id = parent_object_id
        self.parent_object_type = parent_object_type
        self.data = data
        self.summary = summary

    def to_dict(self):
        return {
            'parent_object_id': self.parent_object_id,
            'parent_object_type': self.parent_object_type,
            'summary': self.summary,
            'data': self.data,
            'document_number': self.document_number,
        }
