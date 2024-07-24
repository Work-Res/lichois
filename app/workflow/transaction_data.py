class BaseTransactionData:
    """
    Base class for transaction data containing common attributes.

    Attributes:
        next_activity_name (str): The name of the next activity in the workflow.
        current_status (str): The current status of the application or process.
    """

    def __init__(self, next_activity_name=None, current_status=None):
        self.next_activity_name = next_activity_name
        self.current_status = current_status


class VerificationTransactionData(BaseTransactionData):
    """
    Class for handling verification transaction data.

    Attributes:
        system_verification (str): The result or status of the system verification.
    """

    def __init__(
        self, next_activity_name=None, application_status=None, system_verification=None
    ):
        super().__init__(next_activity_name, application_status)
        self.system_verification = system_verification


class AssessmentTransactionData(BaseTransactionData):
    """
    Class for handling verification transaction data.

    Attributes:
        system_verification (str): The result or status of the system verification.
    """

    def __init__(
        self, next_activity_name=None, application_status=None, system_verification=None
    ):
        super().__init__(next_activity_name, application_status)
        self.system_verification = system_verification


class OfficerTransactionData(BaseTransactionData):
    """
    Class for handling vetting transaction data.

    Attributes:
        verification_decision (str): The decision made during the verification process.
    """

    def __init__(
        self, next_activity_name=None, verification_decision=None, current_status=None
    ):
        super().__init__(next_activity_name, current_status)
        self.verification_decision = verification_decision


class VettingTransactionData(BaseTransactionData):
    """
    Class for handling vetting transaction data.

    Attributes:
        verification_decision (str): The decision made during the verification process.
    """

    def __init__(
        self, next_activity_name=None, verification_decision=None, current_status=None
    ):
        super().__init__(next_activity_name, current_status)
        self.verification_decision = verification_decision
        self.vetting_obj_exists = False


class RecommendationTransitionData(BaseTransactionData):
    """
    Class for handling recommendation transition data.

    Attributes:
        verification_decision (str): The decision made during the verification process.
    """

    def __init__(
        self,
        next_activity_name=None,
        application_status=None,
        verification_decision=None,
    ):
        super().__init__(next_activity_name, application_status)
        self.verification_decision = verification_decision


class ProductionTransactionData(BaseTransactionData):
    """
    Class for handling production transaction data.

    Attributes:
        board_decision (str): The decision made by the board.
        security_clearance (str): The result or status of the security clearance.
        recommendation_decision (str): The decision made during the recommendation process.
    """

    def __init__(
        self,
        board_decision=None,
        security_clearance=None,
        current_status=None,
        next_activity_name=None,
        recommendation_decision=None,
    ):
        super().__init__(next_activity_name, current_status)
        self.board_decision = board_decision
        self.security_clearance = security_clearance
        self.recommendation_decision = recommendation_decision


class AssessmentCaseDecisionTransactionData(BaseTransactionData):
    """
    Class for handling verification transaction data.

    Attributes:
        decision (str)
        role (str)
    """

    def __init__(
        self, next_activity_name=None, application_status=None, decision=None, role=None
    ):
        super().__init__(next_activity_name, application_status)
        self.decision = decision
        self.role = role
