class NewApplicationDTO(object):
    """Represent NewApplicationDTO model submitted by the front-end.

    Attributes:
        process_name (str): The name of the process e.g resident_permit, visa.
        applicant (ApplicationUser): The customer who applying for the given process.
        {
           "process_name": "work",
           "applicant_identifier": "",
           "dob": ""
           "work_place": ""
        }
    """

    def __init__(
        self,
        process_name,
        applicant_identifier: str,
        application_type,
        status=None,
        dob=None,
        work_place=None,
        full_name=None,
        applicant_type=None,
        permit_period=None,
        application_permit_type=None,
        document_number=None,
    ):
        self.proces_name = process_name
        self.full_name = full_name
        self.applicant_identifier = applicant_identifier
        self.status = status
        self.dob = dob
        self.work_place = work_place
        self.application_type = application_type or process_name
        self.applicant_type = applicant_type
        self.permit_period = permit_period
        self.application_permit_type = application_permit_type
        self.document_number = document_number
