

class InterviewCompletionError(Exception):
    """Custom exception for errors during interview completion."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InterviewCompletionError: {self.message}"
