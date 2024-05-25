from rest_framework.exceptions import APIException


class ApplicationRenewalException(APIException):
    status_code = 400
