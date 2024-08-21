

class RabbitMQServiceError(Exception):
    """Custom exception for errors in RabbitMQService."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{self.message} (Caused by {self.original_exception})"
        return self.message
