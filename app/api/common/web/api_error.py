

class APIError:
    """
    Represent an Error Message ocurring during the API call.
    Attributes:
        code:(str) error code
        message(str) : generic error message e.g Something went wrong
        details (?): list of messages, success or error messages, contais very detailed error messages
    """
    def __init__(self, code=None, message=None, details=None):
        self.code = code
        self.message = message
        self.details = details or {}

    def to_dict(self):
        error_dict = {
            'code': self.code,
            'message': self.message,
            'details': self.details
        }
        return error_dict
