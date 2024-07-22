from identifier.identifier import Identifier


class WorkResidentPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "WR"

    @staticmethod
    def process_name():
        return "WORK_RESIDENT_PERMIT"
