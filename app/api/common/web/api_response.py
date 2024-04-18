

class APIResponse:
    """
    Represent an API response object. it is a wrapper class to contain all response objects.
    Attributes:
        status(int) response status code
        messages(str) list of message, success or error messages
        data (?) can be list of objects for anything.
    """
    def __init__(self, status=None, messages=None, data=None):
        self.status = status
        self.messages = messages or []
        self.data = data

    def result(self):
        response_dict = {'status': self.status}
        if self.messages:
            response_dict['messages'] = self.messages
        if self.data is not None:
            response_dict['data'] = self.data
        return response_dict
