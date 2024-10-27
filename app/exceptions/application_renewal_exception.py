from rest_framework.exceptions import APIException


class ApplicationRenewalException(APIException):
    status_code = 400


class ApplicationReplacementException(APIException):
    status_code = 400


class RenewalPeriodNotReached(Exception):
    """
    Exception raised when the permit has not reached the allowable renewal period.
    """

    def __init__(self, message="Permit has not reached allowable renewable period."):
        self.message = message
        super().__init__(self.message)

