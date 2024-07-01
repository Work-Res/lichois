from app_comments.models import Comment


class RequestDeferredApplicationDTO:

    def __init__(self, document_number: str, comment: Comment, deferred_from: str, batch_id: str,
                 expected_action: str = None, task_details_config_file=None):
        self.document_number = document_number
        self.comment = comment
        self.deferred_from = deferred_from
        self.expected_action = expected_action
        self.task_details_config_file = task_details_config_file
        self.batch_id = batch_id
