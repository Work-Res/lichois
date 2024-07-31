

class BatchNotFoundException(Exception):
    def __init__(self, message="Batch not found"):
        self.message = message
        super().__init__(self.message)


class ApplicationNotFoundException(Exception):
    def __init__(self, message="Application not found"):
        self.message = message
        super().__init__(self.message)


class BatchApplicationNotFoundException(Exception):
    def __init__(self, message="BatchApplication not found"):
        self.message = message
        super().__init__(self.message)


class InvalidBatchStatusException(Exception):
    def __init__(self, message="Invalid batch status"):
        self.message = message
        super().__init__(self.message)


class ApplicationNotFoundException(Exception):
    def __init__(self, message="Application not found"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class LegalAssessmentNotFoundException(Exception):
    def __init__(self, message="Legal assessment not found"):
        self.message = message
        super().__init__(self.message)
