class PermitProductionException(Exception):
    def __init__(self, message="Failed to create permit production."):
        self.message = message
        super().__init__(self.message)
