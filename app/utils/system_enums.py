from enum import Enum


class ApplicationProcesses(Enum):
    VISA = "VISA"
    WORK_RESIDENT_PERMIT = "WORK_RESIDENT_PERMIT"
    WORK_PERMIT = "WORK_PERMIT"
    RESIDENT_PERMIT = "RESIDENT_PERMIT"
    SPECIAL_PERMIT = "SPECIAL_PERMIT"


class ApplicationStatuses(Enum):
    NEW = "NEW"
    DRAFT = "DRAFT"
    VERIFICATION = "VERIFICATION"
    VETTING = "VETTING"
    COMMITEE_EVALUATION = "COMMITEE_EVALUATION"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
    RECOMMENDATION = "RECOMMENDATION"


class WorkflowEnum(Enum):
    RECOMMENDATION = "RECOMMENDATION"
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
    
    
class ApplicationTypesEnum(Enum):
    WORK_RES_APPEAL_PERMIT = "WORK_RES_APPEAL_PERMIT"
    WORK_RES_CANCELLATION_PERMIT = "WORK_RES_CANCELLATION_PERMIT"
    WORK_RES_EMERGENCY_PERMIT = "WORK_RES_EMERGENCY_PERMIT"
    WORK_RES_EXEMPTION_PERMIT = "WORK_RES_EXEMPTION_PERMIT"
    WORK_RES_RENEWAL_PERMIT = "WORK_RES_RENEWAL_PERMIT"
    WORK_RES_REPLACEMENT_PERMIT = "WORK_RES_REPLACEMENT_PERMIT"
    RESIDENT_PERMIT = "RESIDENT_PERMIT"
    WORK_PERMIT = "WORK_PERMIT"
    WORK_RESIDENT_PERMIT = "WORK_RESIDENT_PERMIT"
    
