

class RenewalApplicationDTO(object):

    def __init__(self, process_name, applicant_identifier, document_number, work_place=None, application_type=None):
        self.proces_name = process_name
        self.applicant_identifier = applicant_identifier
        self.document_number = document_number
        self.work_place = work_place
        self.application_type = application_type
