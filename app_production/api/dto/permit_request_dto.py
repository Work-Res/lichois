class PermitRequestDTO:

    def __init__(
        self,
        document_number=None,
        permit_type=None,
        date_issued=None,
        date_expiry=None,
        place_issue=None,
        security_number=None,
        permit_no=None,
        application_type=None,
    ):
        self.document_number = document_number
        self.permit_type = permit_type
        self.permit_no = permit_no
        self.date_issued = date_issued
        self.date_expiry = date_expiry
        self.place_issue = place_issue
        self.security_number = security_number
        self.application_type = application_type
