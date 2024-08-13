import logging

from app.utils.system_enums import ApplicationDecisionEnum
from app_comments.models.comment import Comment
from app_decision.services import ApplicationDecisionService


class TravelCertificateDecisionService(ApplicationDecisionService):

    def __init__(
        self,
        document_number,
        comment: Comment = None,
        decision_value=None,
        application=None,
    ):
        super().__init__(document_number, comment, application)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.decision_value = decision_value

    def decision_predicate(self):
        self.logger.error(
            f"decision_value: {self.decision_value} and {ApplicationDecisionEnum.ACCEPTED.value}"
        )
        return (
            self.decision_value.upper()
            == ApplicationDecisionEnum.ACCEPTED.value.upper()
        )
