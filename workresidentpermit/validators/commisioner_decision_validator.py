from app.api.common.web import APIResponse, APIMessage

from app.models import ApplicationVerification
from app.utils import ApplicationDecisionEnum


class CommissionerDecisionValidator:
    """
    Responsible for validating all mandatory for commissioner's decision.
    """

    def __init__(self, document_number: str):
        self.document_number = document_number
        self.response = APIResponse()

    def validate(self):
        """
        Check if all required is available for the commissioner is captured.
        """
        try:
            ApplicationVerification.objects.get(
                document_number=self.document_number,
                decision__code__iexact=ApplicationDecisionEnum.ACCEPTED.value
            )
        except ApplicationVerification.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="The verification must be accepted.",
                    details="The application verification must be accepted before commercing with commissioner "
                            "decision. "
                ).to_dict()
            )

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.validate()
        return True if len(self.response.messages) == 0 else False
