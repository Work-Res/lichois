from identifier.identifier import Identifier


class VisaPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "visapermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "VS"

    @staticmethod
    def process_name():
        return "VISA_PERMIT"
