import logging
from app.models import Application
from app_checklist.models import SystemParameterPayment


class PaymentValidator:
    """
    Validates if a payment fee is applicable for a given application.
    """

    def __init__(self, document_number, application=None):
        self.document_number = document_number
        self.application = application
        self.logger = logging.getLogger(__name__)

    def _get_application(self):
        """
        Retrieves the application associated with the document number.
        If the application is already provided, it skips fetching from the database.
        """
        if self.application:
            self.logger.debug(f"Using provided application for document number: {self.document_number}")
            return self.application

        try:
            self.application = Application.objects.get(
                application_document__document_number=self.document_number
            )
            self.logger.info(f"Application retrieved for document number: {self.document_number}")
            return self.application
        except Application.DoesNotExist:
            self.logger.warning(f"No application found for document number: {self.document_number}")
            return None
        except Exception as e:
            self.logger.error(
                f"Unexpected error retrieving application for document number {self.document_number}: {e}")
            raise

    def has_payment_fee(self):
        """
        Checks if a payment fee is applicable for the application's type.
        Returns True if a payment fee exists, otherwise False.
        """
        try:
            application = self._get_application()
            if not application:
                self.logger.warning(
                    f"Cannot determine payment fee, no application found for document number: {self.document_number}")
                return False

            SystemParameterPayment.objects.get(application_type=application.process_name)
            self.logger.info(f"Payment fee applicable for application type: {application.application_type}")
            return True
        except SystemParameterPayment.DoesNotExist:
            self.logger.info(f"No payment fee found for application type: {self.application.application_type}")
            return False
        except Exception as e:
            self.logger.error(f"Error checking payment fee for document number {self.document_number}: {e}")
            raise
