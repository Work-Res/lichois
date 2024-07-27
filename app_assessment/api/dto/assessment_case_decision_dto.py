

class AssessmentCaseDecisionDTO:

    def __init__(self, parent_object_id=None, parent_object_type=None,
                 author=None,
                 author_role=None,
                 decision=None,
                 document_number=None
                 ):
        self.document_number = document_number
        self.parent_object_id = parent_object_id
        self.parent_object_type = parent_object_type
        self.author = author
        self.author_role = author_role
        self.decision = decision
