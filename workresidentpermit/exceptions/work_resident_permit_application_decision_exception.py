class WorkResidentPermitApplicationDecisionException(Exception):

    def __init__(
        self, message="Something went wrong, work permit application decision."
    ):
        self.message = message
        super().__init__(self.message)
