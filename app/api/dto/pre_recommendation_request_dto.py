from .request_dto import RequestDTO


class PresRecommendationRequestDTO(RequestDTO):

    def __init__(
        self,
        document_number=None,
        status=None,
        summary=None,
        user=None,
        comment_type=None,
        role=None,
        **kwargs,
    ):
        super().__init__(
            document_number=document_number,
            status=status,
            summary=summary,
            user=user,
            comment_type=comment_type,
            **kwargs
        )
        self.role = role
