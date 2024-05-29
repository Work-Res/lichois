

class SecurityClearanceRequestDTO:

    def __init__(self, document_number=None, status=None, summary=None):

        self.document_number = document_number
        self.status = status
        self.summary = summary
