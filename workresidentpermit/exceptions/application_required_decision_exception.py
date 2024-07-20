class ApplicationRequiredDecisionException(Exception):
    def __init__(
        self,
        message="A application is required and cannot be None for creating application decision.",
    ):
        self.message = message
        super().__init__(self.message)
