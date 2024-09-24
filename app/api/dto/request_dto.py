class RequestDTO:

    def __init__(
        self,
        document_number=None,
        status=None,
        summary=None,
        user=None,
        comment_type=None,
        **kwargs,
    ):
        self.document_number = document_number
        self.status = status
        self.summary = summary
        self.comment_type = comment_type
        self.user = user
        for key, value in kwargs.items():
            setattr(self, key, value)
