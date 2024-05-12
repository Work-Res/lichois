

class WorkflowTransition:

    def __init__(self, previous_status, current_status=None, next_activity_name=None):
        self.previous_status = previous_status
        self.current_status = current_status
        self.next_activity_name = next_activity_name
