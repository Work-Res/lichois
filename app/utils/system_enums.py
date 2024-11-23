from enum import Enum


class ApplicationProcesses(Enum):
    VISA_PERMIT = "VISA_PERMIT"
    WORK_RESIDENT_PERMIT = "WORK_RESIDENT_PERMIT"
    WORK_RESIDENT_PERMIT_REPLACEMENT = "WORK_RESIDENT_PERMIT_REPLACEMENT"
    WORK_RESIDENT_PERMIT_RENEWAL = "WORK_RESIDENT_PERMIT_RENEWAL"
    WORK_RESIDENT_VARIATION = "WORK_RESIDENT_VARIATION"
    WORK_PERMIT = "WORK_PERMIT"
    WORK_PERMIT_REPLACEMENT = "WORK_PERMIT_REPLACEMENT"
    RESIDENT_PERMIT = "RESIDENT_PERMIT"
    RESIDENT_PERMIT_REPLACEMENT = "RESIDENT_PERMIT_REPLACEMENT"
    SPECIAL_PERMIT = "SPECIAL_PERMIT"
    APPEAL_PERMIT = "APPEAL_PERMIT"
    EXEMPTION_CERTIFICATE = "EXEMPTION_CERTIFICATE"
    BLUE_CARD_PERMIT = "BLUE_CARD_PERMIT"
    BLUE_CARD_RETURNS = "BLUE_CARD_RETURNS"
    BLUE_CARD_REPLACEMENT = "BLUE_CARD_REPLACEMENT"
    TRAVEL_CERTIFICATE = "TRAVEL_CERTIFICATE"
    PERMANENT_RESIDENCE = "PERMANENT_RESIDENCE"
    PERMANENT_RESIDENCE_REPLACEMENT = "PERMANENT_RESIDENCE_REPLACEMENT"
    PERMANENT_RESIDENCE_RETURNS = "PERMANENT_RESIDENCE_RETURNS"


class ApplicationStatusEnum(Enum):
    NEW = "NEW"
    DRAFT = "DRAFT"
    VERIFICATION = "VERIFICATION"
    VETTING = "VETTING"
    ASSESSMENT = "ASSESSMENT"
    REVIEW = "REVIEW"
    COMMITEE_EVALUATION = "COMMITEE_EVALUATION"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
    RECOMMENDATION = "RECOMMENDATION"
    MINISTER_DECISION = "MINISTER_DECISION"
    DEFERRED = "DEFERRED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


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
    DONE = "Done"
