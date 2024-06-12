

class WorkflowTransition:

    def __init__(self, previous_status=None, current_status=None, next_activity_name=None,
                 previous_business_decision=None, application_status=None, system_verification=None):
        self.previous_status = previous_status
        self.current_status = current_status
        self.next_activity_name = next_activity_name
        self.previous_business_decision = previous_business_decision
        self.application_status = application_status
        self.system_verification = system_verification
