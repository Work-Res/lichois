

class WorkflowProductionRequiredDecisionException(Exception):
    def __init__(self,
                 message="A workflow productionData is require, and cannot be None for creating application decision."):
        self.message = message
        super().__init__(self.message)
