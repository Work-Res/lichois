from identifier.identifier import Identifier

from app.utils.system_enums import ApplicationProcesses
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class SpecialPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return ApplicationProcesses.SPECIAL_PERMIT.value


class SpecialPermitIdentifierCancellation(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "CA"

    @staticmethod
    def process_name():
        return (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_CANCELLATION.value
        )


class SpecialPermitIdentifierRenewal(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "RW"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_RENEWAL.value


class SpecialPermitIdentifierEmergency(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "EM"

    @staticmethod
    def process_name():
        return (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_EMERGENCY.value
        )


class SpecialPermitIdentifierExemptionCertificate(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "EX"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE.value


class SpecialPermitIdentifierAppeal(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "AP"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.value
