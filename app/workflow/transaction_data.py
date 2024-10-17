class BaseTransactionData:
    """
    Base class for transaction data containing common attributes.

    Attributes:
        next_activity_name (str): The name of the next activity in the workflow.
        current_status (str): The current status of the application or process.
    """

    def __init__(self, next_activity_name=None, current_status=None, status=None):
        self.next_activity_name = next_activity_name
        self.current_status = current_status
        self.status = status


class VerificationTransactionData(BaseTransactionData):
    """
    Class for handling verification transaction data.

    Attributes:
        system_verification (str): The result or status of the system verification.
    """

    def __init__(
        self, next_activity_name=None, application_status=None, system_verification=None
    ):
        super().__init__(
            next_activity_name, application_status, status=system_verification
        )
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
        super().__init__(
            next_activity_name, application_status, status=system_verification
        )
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
        super().__init__(
            next_activity_name, current_status, status=verification_decision
        )
        self.verification_decision = verification_decision


class VettingTransactionData(BaseTransactionData):
    """
    Class for handling vetting transaction data.

    Attributes:
        verification_decision (str): The decision made during the verification process.
    """

    def __init__(
        self,
        next_activity_name=None,
        vetting_decision=None,
        current_status=None,
        vetting_obj_exists=None,
    ):
        super().__init__(next_activity_name, current_status, status=vetting_decision)
        self.vetting_decision = vetting_decision
        self.vetting_obj_exists = vetting_obj_exists


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
        recommendation_decision=None,
        security_clearance=None,
    ):
        super().__init__(
            next_activity_name, application_status, status=recommendation_decision
        )
        self.recommendation_decision = recommendation_decision
        self.security_clearance = security_clearance


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
        minister_decision=None,
    ):
        super().__init__(
            next_activity_name, current_status, status=recommendation_decision
        )
        self.board_decision = board_decision
        self.security_clearance = security_clearance
        self.recommendation_decision = recommendation_decision
        self.minister_decision = minister_decision


class AssessmentCaseDecisionTransactionData(BaseTransactionData):

    def __init__(
        self,
        next_activity_name=None,
        application_status=None,
        assessment_decision=None,
        security_clearance=None,
    ):
        super().__init__(
            next_activity_name, application_status, status=assessment_decision
        )
        self.assessment_decision = assessment_decision


class ReviewCaseDecisionTransactionData(BaseTransactionData):

    def __init__(
        self,
        next_activity_name=None,
        application_status=None,
        review_decision=None,
        security_clearance=None,
    ):
        super().__init__(next_activity_name, application_status, status=review_decision)
        self.review_decision = review_decision


class MinisterDecisionTransactionData(BaseTransactionData):
    def __init__(
        self, next_activity_name=None, application_status=None, minister_decision=None
    ):
        super().__init__(
            next_activity_name, application_status, status=minister_decision
        )
        self.minister_decision = minister_decision


class GazetteTransactionData(BaseTransactionData):
    def __init__(
        self, next_activity_name=None, application_status=None, gazette_completed=None, vetting_obj_exists=None
    ):
        super().__init__(
            next_activity_name, application_status
        )
        self.gazette_completed = gazette_completed
        self.vetting_obj_exists = vetting_obj_exists


class RecommendationDecisionTransactionData(BaseTransactionData):
    def __init__(
        self,
        next_activity_name=None,
        application_status=None,
        recommendation_decision=None,
    ):
        super().__init__(next_activity_name, application_status)
        self.recommendation_decision = recommendation_decision


class PresRecommendationDecisionTransactionData(BaseTransactionData):
    def __init__(
        self,
        next_activity_name=None,
        application_status=None,
        recommendation_decision=None,
        role=None
    ):
        super().__init__(next_activity_name, application_status)
        self.recommendation_decision = recommendation_decision
        self.role = role


class PresidentDecisionTransactionData(BaseTransactionData):
    def __init__(
        self, next_activity_name=None, application_status=None, president_decision=None
    ):
        super().__init__(
            next_activity_name, application_status, status=president_decision
        )
        self.president_decision = president_decision


class ForeignRenunciationDecisionTransactionData(BaseTransactionData):
    def __init__(
        self, next_activity_name=None, application_status=None, renunciation_decision=None
    ):
        super().__init__(
            next_activity_name, application_status, status=renunciation_decision
        )
        self.renunciation_decision = renunciation_decision
