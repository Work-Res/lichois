from identifier.identifier import Identifier

from app.utils import ApplicationProcesses


class WorkResidentPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "WR"

    @staticmethod
    def process_name():
        return ApplicationProcesses.WORK_RESIDENT_PERMIT.value


class WorkResidentPermitReplacementIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "WR"

    @staticmethod
    def process_name():
        return ApplicationProcesses.WORK_RESIDENT_PERMIT_REPLACEMENT.value


class WorkPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "R"

    @staticmethod
    def process_name():
        return ApplicationProcesses.WORK_PERMIT.value


class WorkPermitReplacementIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "R"

    @staticmethod
    def process_name():
        return ApplicationProcesses.WORK_PERMIT_REPLACEMENT.value


class ResidentPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "W"

    @staticmethod
    def process_name():
        return ApplicationProcesses.RESIDENT_PERMIT.value


class ResidentPermitReplacementIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "W"

    @staticmethod
    def process_name():
        return ApplicationProcesses.RESIDENT_PERMIT_REPLACEMENT.value
