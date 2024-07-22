from identifier.identifier import Identifier

from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class SpecialPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.value


class SpecialPermitIdentifierCancellation(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_CANCELLATION.value
        )


class SpecialPermitIdentifierRenewal(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_RENEWAL.value


class SpecialPermitIdentifierEmergency(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_EMERGENCY.value
        )


class SpecialPermitIdentifierExemptionCertificate(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE.value


class SpecialPermitIdentifierTravelCertificate(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "workresidentpermit"
    identifier_type = "SP"

    @staticmethod
    def process_name():
        return WorkResidentPermitApplicationTypeEnum.TRAVEL_CERTIFICATE.value
