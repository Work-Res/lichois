from enum import Enum


class WorkResidentPermitApplicationTypeEnum(Enum):

    WORK_PERMIT_ONLY = "WORK_PERMIT_ONLY"
    WORK_PERMIT_EMERGENCY = "WORK_PERMIT_EMERGENCY"
    WORK_PERMIT_CANCELLATION = "WORK_PERMIT_CANCELLATION"
    WORK_PERMIT_REPLACEMENT = "WORK_PERMIT_REPLACEMENT"
    WORK_PERMIT_APPEAL = "WORK_PERMIT_APPEAL"
    WORK_PERMIT_RENEWAL = "WORK_PERMIT_RENEWAL"

    RESIDENT_PERMIT_ONLY = "RESIDENT_PERMIT_ONLY"
    RESIDENT_PERMIT_EMERGENCY = "RESIDENT_PERMIT_EMERGENCY"
    RESIDENT_PERMIT_CANCELLATION = "RESIDENT_PERMIT_CANCELLATION"
    RESIDENT_PERMIT_REPLACEMENT = "RESIDENT_PERMIT_REPLACEMENT"
    RESIDENT_PERMIT_APPEAL = "RESIDENT_PERMIT_APPEAL"
    RESIDENT_PERMIT_RENEWAL = "RESIDENT_PERMIT_RENEWAL"

    WORK_RESIDENT_PERMIT_ONLY = "WORK_RESIDENT_PERMIT_ONLY"
    WORK_RESIDENT_PERMIT_EMERGENCY = "WORK_RESIDENT_PERMIT_EMERGENCY"
    WORK_RESIDENT_PERMIT_CANCELLATION = "WORK_RESIDENT_PERMIT_CANCELLATION"
    WORK_RESIDENT_PERMIT_REPLACEMENT = "WORK_RESIDENT_PERMIT_REPLACEMENT"
    WORK_RESIDENT_PERMIT_APPEAL = "WORK_RESIDENT_PERMIT_APPEAL"
    WORK_RESIDENT_PERMIT_RENEWAL = "WORK_RESIDENT_PERMIT_RENEWAL"

    EXEMPTION_CERTIFICATE = "EXEMPTION_CERTIFICATE_ONLY"
    EXEMPTION_CERTIFICATE_APPEAL = "EXEMPTION_CERTIFICATE_APPEAL"
    EXEMPTION_CERTIFICATE_CANCELLATION = "EXEMPTION_CERTIFICATE_CANCELLATION"
    EXEMPTION_CERTIFICATE_REPLACEMENT = "EXEMPTION_CERTIFICATE_REPLACEMENT"
    EXEMPTION_CERTIFICATE_RENEWAL = "EXEMPTION_CERTIFICATE_RENEWAL"
