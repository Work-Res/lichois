from haystack import indexes

from app.models import ApplicationVersion, ApplicationVerification
from workresidentpermit.models import SecurityClearance
from board.models import BoardDecision


class ApplicationVersionIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    TODO: Not the best solution, requires refactoring
    """

    document_number = indexes.CharField(model_attr='application__application_document__document_number')

    application_type = indexes.CharField(model_attr='application__application_type')

    submission_date = indexes.DateField(model_attr='application__submission_date')

    application_status = indexes.CharField(model_attr='application__application_status__code')

    full_name = indexes.CharField(model_attr='application__application_document__applicant__full_name')

    user_identifier = indexes.CharField(model_attr='application__application_document__applicant__user_identifier')

    verification_status = indexes.CharField()

    security_clearance_status = indexes.CharField()

    board_decision = indexes.CharField()

    status = indexes.CharField()

    def prepare_verification_status(self, obj):
        try:
            verification = ApplicationVerification.objects.get(
                document_number=obj.application.application_document.document_number)
            return verification.decision
        except ApplicationVerification.DoesNotExist:
            return 'pending'

    def prepare_security_clearance_status(self, obj):
        try:
            security_clearance = SecurityClearance.objects.get(
                document_number=obj.application.application_document.document_number)
            return security_clearance.status
        except SecurityClearance.DoesNotExist:
            return 'pending'

    def prepare_board_decision(self, obj):
        try:
            board_decision = BoardDecision.objects.get(
                assessed_application__application_document__document_number=
                obj.application.application_document.document_number)
            return board_decision.decision_outcome
        except SecurityClearance.DoesNotExist:
            return 'pending'

    class Meta:
        model = ApplicationVersion
