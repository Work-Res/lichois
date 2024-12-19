import logging
from django.core.exceptions import ValidationError
from app_payments.models import Payment
from app_payments.service import PaymentDecisionHandlerService
from app_payments.validator import SignatureValidator


class CyberSourceResponseProcessor:
    """
    Processes the CyberSource payment response.
    """

    def __init__(self, response_data):
        self.response_data = response_data
        self.logger = logging.getLogger(__name__)

    def process_response(self):
        """
        Processes the payment response and updates the payment record.
        """
        try:
            self.logger.info("Starting CyberSource payment response processing.")

            # Validate the response signature
            SignatureValidator.validate(self.response_data)

            # Extract response fields
            reference_number = self.response_data.get('req_reference_number')
            decision = self.response_data.get('decision')
            reason_code = self.response_data.get('reason_code')
            transaction_id = self.response_data.get('transaction_id')

            self.logger.info(f"Processing payment for reference number: {reference_number}")

            # Retrieve payment
            payment = self._get_payment(reference_number)

            # Handle the payment decision
            decision_handler = PaymentDecisionHandlerService(payment)
            decision_handler.handle_decision(decision, reason_code, transaction_id)

        except ValidationError as e:
            self.logger.error(f"Validation error while processing response: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error processing CyberSource payment response: {e}")
            raise

    def _get_payment(self, reference_number):
        """
        Retrieves the Payment object based on the reference number.
        """
        try:
            return Payment.objects.get(reference_number=reference_number)
        except Payment.DoesNotExist:
            self.logger.error(f"Payment not found for reference number: {reference_number}")
            raise ValidationError(f"Payment not found for reference number: {reference_number}")
