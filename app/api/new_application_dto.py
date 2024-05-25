

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
    def __init__(self, process_name, applicant_identifier, status, dob=None, work_place=None, full_name=None):
        self.proces_name = process_name
        self.full_name = full_name
        self.applicant_identifier = applicant_identifier
        self.status = status
        self.dob = dob
        self.work_place = work_place
