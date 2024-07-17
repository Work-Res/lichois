

class IdentifierConfigNotFound(Exception):
    """A custom exception class."""
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
