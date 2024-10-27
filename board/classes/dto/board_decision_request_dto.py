from app.api.dto.request_dto import RequestDTO


class BoardDecisionRequestDTO(RequestDTO):

    def __init__(
        self,
        document_number=None,
        status=None,
        summary=None,
        user=None,
        comment_type=None,
        board_decision=None,
        **kwargs,
    ):
        super().__init__(
            document_number=document_number,
            status=status,
            summary=summary,
            user=user,
            comment_type=comment_type,
            board_decision=board_decision,
            **kwargs,
        )
