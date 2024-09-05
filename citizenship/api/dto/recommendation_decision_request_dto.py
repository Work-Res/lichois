from app.api.dto.request_dto import RequestDTO


class RecommendationDecisionRequestDTO(RequestDTO):

    def __init__(
        self,
        document_number=None,
        status=None,
        summary=None,
        user=None,
        role=None,
        **kwargs,
    ):
        super().__init__(
            document_number=document_number,
            status=status,
            summary=summary,
            user=user,
            **kwargs,
        )
        self.role = role
