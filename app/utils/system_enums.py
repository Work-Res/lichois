from enum import Enum


class ApplicationProcesses(Enum):
    VISA = "VISA"
    WORK_RESIDENT_PERMIT = "WORK_RESIDENT_PERMIT"
    WORK_PERMIT = "WORK_PERMIT"
    RESIDENT_PERMIT = "RESIDENT_PERMIT"


class ApplicationStatuses(Enum):
    NEW = "NEW"
    DRAFT = "DRAFT"
    VERIFICATION = "VERIFICATION"
    VETTING = "VETTING"
    COMMITEE_EVALUATION = "COMMITEE_EVALUATION"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"


class WorkflowEnum(Enum):
    VERIFICATION = "VERIFICATION"
    VETTING = "VETTING"
    FINAL_DECISION = "FINAL_DECISION"
    PERMIT_CANCELLATION = "PERMIT_CANCELLATION"
    END = "END"


class ApplicationDecisionEnum(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    APPROVED = "approved"
    DEFERRED = "deferred"
