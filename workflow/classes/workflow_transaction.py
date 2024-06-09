

class WorkflowTransition:

    def __init__(self, previous_status, current_status=None, next_activity_name=None, previous_business_decision=None):
        self.previous_status = previous_status
        self.current_status = current_status
        self.next_activity_name = next_activity_name
        self.previous_business_decision = previous_business_decision
