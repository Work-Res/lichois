from enum import Enum


class PaymentStatusEnum(Enum):
    ACCEPT = "ACCEPT"
    DECLINE = "DECLINE"
    CANCEL = "CANCEL"

    @classmethod
    def choices(cls):
        """
        Provides a tuple of choices for use in Django model fields.
        """
        return [(status.name, status.value) for status in cls]

    @classmethod
    def has_value(cls, value):
        """
        Checks if a given value is a valid enum value.
        """
        return value in cls._value2member_map_
