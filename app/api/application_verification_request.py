

class ApplicationVerificationRequest:

    def __init__(self, decision=None, comment=None, outcome_reason=None):
        self.decision = decision
        self.comment = comment
        self.outcome_reason = outcome_reason
