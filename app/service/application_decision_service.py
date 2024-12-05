import logging
from abc import abstractmethod

from django.shortcuts import get_object_or_404

from app_comments.models import Comment
from workresidentpermit.exceptions import (
    ApplicationRequiredDecisionException,
    WorkResidentPermitApplicationDecisionException,
)

from ..models import ApplicationDecision, ApplicationDecisionType
from .create_dependent_application_decision_service import (
    CreateDependentApplicationDecisionService,
)


class ApplicationDecisionService(CreateDependentApplicationDecisionService):
    """Responsible for create application decision based on security clearance or board decision."""

    def __init__(
        self,
        document_number,
        comment: Comment = None,
        decision_value=None,
    ):
        self.document_number = document_number
        self.comment = comment
        self.decision_value = decision_value
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def decision_predicate(self):
        """
        Evaluate required business rules for production, and returns True or False for creating application decision.
        Please override this method on based class for decision making
        :return: True or False.
        """
        print("Running running running..")
        return False

    def proposed_application_decision_type(self) -> ApplicationDecisionType:
        try:
            proposed_application_decision_type = get_object_or_404(
                ApplicationDecisionType, code__iexact=self.decision_value
            )
            return proposed_application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            error_message = f"Application decision type cannot be found using decision_type: {self.decision_value}"
            self.logger.error(error_message)
            raise WorkResidentPermitApplicationDecisionException(error_message)

    def create_application_decision(self):
        if self.decision_predicate():
            decision, _ = ApplicationDecision.objects.get_or_create(
                document_number=self.document_number,
                defaults={
                    "final_decision_type": None,
                    "proposed_decision_type": self.proposed_application_decision_type(),
                    "comment": self.comment,
                },
            )
            self.logger.info(
                f"Application decision created successfully for {self.document_number}"
            )
            # self.create_dependents_application_decision(
            #     document_number=self.document_number
            # )
        else:
            print(f"Not within the predicate: {self.document_number}")
