from enum import Enum


class ApplicationProcesses(Enum):
    VISA = "VISA"
    WORK_RESIDENT_PERMIT = "WORK_RESIDENT_PERMIT"


class ApplicationStatuses(Enum):
    NEW = "NEW"
    DRAFT = "DRAFT"
    VERIFICATION = "VERIFICATION"
    VETTING = "VETTING"
    COMMITEE_EVALUATION = "COMMITEE_EVALUATION"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
