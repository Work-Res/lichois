from app_comments.models import Comment


class RequestDeferredApplicationDTO:

    def __init__(self, document_number: str, comment: Comment):
        self.document_number = document_number
        self.comment = comment
