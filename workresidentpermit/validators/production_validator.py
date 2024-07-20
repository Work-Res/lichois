from app_decision.models import ApplicationDecision
from app.utils import ApplicationDecisionEnum

from app.api.common.web import APIResponse, APIMessage


class ProductionValidator:
    """
    Responsible for validating all mandatory for work permit.
    """

    def __init__(self, document_number: str):
        self.document_number = document_number
        self.response = APIResponse()

    def validate(self):
        """
        Check if the application is at the production stage.
        """
        try:
            ApplicationDecision.objects.get(
                document_number=self.document_number,
                proposed_decision_type__code__iexact=ApplicationDecisionEnum.ACCEPTED.value,
            )
        except ApplicationDecision.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Production is not ready.",
                    details="The permit production is expected when the application has been taken.",
                ).to_dict()
            )

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.validate()
        return True if len(self.response.messages) == 0 else False
