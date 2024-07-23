from enum import Enum


class VerificationStatusEnum(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    VALIDATED = "VALIDATED"
