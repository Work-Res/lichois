from app_payments.models import Payment
from django.core.exceptions import ValidationError


class PaymentDecisionHandlerService:
    """
    Handles the decision logic for CyberSource payment responses.
    """

    def __init__(self, payment):
        self.payment = payment

    def handle_decision(self, decision, reason_code, transaction_id):
        """
        Handles the payment decision and updates the payment status.
        """
        if decision == 'ACCEPT':
            self._update_status(Payment.STATUS_PAID, transaction_id)
        elif decision == 'DECLINE':
            self._update_status(Payment.STATUS_FAILED, transaction_id, reason=f"Declined (Reason Code: {reason_code})")
        elif decision == 'CANCEL':
            self._update_status(Payment.STATUS_CANCELLED, transaction_id)
        else:
            raise ValidationError(f"Unexpected decision: {decision}")

    def _update_status(self, status, transaction_id, reason=None):
        """
        Updates the payment status and transaction ID.
        """
        self.payment.status = status
        self.payment.transaction_id = transaction_id
        if reason:
            self.payment.description = reason
        self.payment.save()
