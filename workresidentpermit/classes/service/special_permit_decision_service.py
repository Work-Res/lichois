import logging
from app.models import Application
from app.utils import ApplicationDecisionEnum
from app_comments.models import Comment
from workresidentpermit.workflow import ProductionTransactionData
from .application_decision_service import ApplicationDecisionService
from ..config.configuration_loader import BaseConfigLoader
from ..config.decision_loader import DecisionLoader
from workresidentpermit.models import CommissionerDecision, MinisterDecision, SecurityClearance


class SpecialPermitDecisionService(DecisionLoader, ApplicationDecisionService):
    """ Responsible for creating an application decision based on commissioner or minister decisions. """

    def __init__(self, document_number, comment: Comment = None, config_loader: BaseConfigLoader = None):
        # Initialize DecisionLoader with document_number
        DecisionLoader.__init__(self, document_number=document_number)

        # Initialize ApplicationDecisionService with document_number and comment
        ApplicationDecisionService.__init__(self, document_number=document_number, comment=comment)

        self.document_number = document_number
        self.application = Application.objects.get(application_document__document_number=document_number)
        self.workflow = ProductionTransactionData()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.decision_value = None
        self.approval_processes = self._load_approval_processes(config_loader)
        self._security_clearance = self.security_clearance()
        

    @staticmethod
    def _load_approval_processes(config_loader: BaseConfigLoader):
        """ Load approval processes using the provided config loader. """
        process_names = config_loader.load() if config_loader else []
        return process_names

    # return [getattr(WorkResidentPermitApplicationTypeEnum.value, process.strip()) for process in process_names]

    def decision_predicate(self):
        """ Determine the final decision based on commissioner and/or minister decisions. """
        is_commissioner_accepted = self.is_decision_accepted(CommissionerDecision)
        is_minister_accepted = self.is_decision_accepted(MinisterDecision)
        requires_approval = self.application.application_type in self.approval_processes
        self.logger.info(f"Commissioner decision: {is_commissioner_accepted}, Minister decision: {is_minister_accepted}, ")

        if requires_approval:
            if is_commissioner_accepted and is_minister_accepted:
                self.set_decision(ApplicationDecisionEnum.ACCEPTED)
                self.workflow.recommendation_decision = ApplicationDecisionEnum.ACCEPTED.value.upper()
                return True
            elif is_minister_accepted:
                self.set_decision(ApplicationDecisionEnum.ACCEPTED)
                self.workflow.recommendation_decision = ApplicationDecisionEnum.ACCEPTED.value.upper()
                return True
        else:
            if is_commissioner_accepted and self._security_clearance:
                if self._security_clearance.status.code.lower() == ApplicationDecisionEnum.ACCEPTED.value.lower():
                    self.set_decision(ApplicationDecisionEnum.ACCEPTED)
                else:
                    self.set_decision(ApplicationDecisionEnum.REJECTED)
                self.workflow.recommendation_decision = ApplicationDecisionEnum.ACCEPTED.value.upper()
                self.workflow.security_clearance = self._security_clearance.status.code.upper()
                return True
            elif is_commissioner_accepted:
                self.set_decision(ApplicationDecisionEnum.ACCEPTED)
                self.workflow.recommendation_decision = ApplicationDecisionEnum.ACCEPTED.value.upper()
                return True

        # If neither condition is met, reject the application
        if self.get_decision(CommissionerDecision) or (self.get_decision(MinisterDecision) and requires_approval):
            self.set_decision(ApplicationDecisionEnum.REJECTED)
            self.workflow.recommendation_decision = ApplicationDecisionEnum.REJECTED.value.upper()
            return True

    def set_decision(self, decision_enum):
        """ Set the decision value. """
        self.decision_value = decision_enum.value
        
    def security_clearance(self):
        try:
            return SecurityClearance.objects.get(
                document_number=self.document_number
            )
        except SecurityClearance.DoesNotExist:
            self.logger.info(f"Security clearance is pending for {self.document_number}")
