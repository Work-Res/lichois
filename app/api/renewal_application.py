

class RenewalApplication(object):

    """Represent RenewalApplication model submitted by the front-end.

        Attributes:
            process_name (str): The name of the process e.g resident_permit, visa.
            applicant (ApplicationUser): The customer who applying for the given process.
            {
               "process_name": "work",
               "applicant_identifier": "",
               "status": ""
               "work_place": ""
               "document_number": ""
            }
    """
    def __init__(self, process_name, applicant_identifier, document_number, work_place=None):
        self.proces_name = process_name
        self.applicant_identifier = applicant_identifier
        self.document_number = document_number
        self.work_place = work_place
