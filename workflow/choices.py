from enum import Enum


class TaskStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"


class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
