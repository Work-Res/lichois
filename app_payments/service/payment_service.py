import logging
import uuid
from datetime import date
from django.db import transaction

from app.models import Application
from app_checklist.models import SystemParameterPayment
from app_payments.models import Payment
from app_payments.validator import PaymentValidator


class PaymentService:
    """
    Service class for handling payment-related operations.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_payment_by_document_number(self, document_number):
        """
        Retrieves a Payment object by its document number.
        """
        try:
            payment = Payment.objects.get(document_number=document_number)
            self.logger.info(f"Payment retrieved successfully for document number: {document_number}")
            return payment
        except Payment.DoesNotExist:
            self.logger.warning(f"No payment found for document number: {document_number}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving payment for document number {document_number}: {e}")
            raise

    @transaction.atomic
    def get_or_create_payment(self, document_number, amount, reference_number, **kwargs):
        """
        Retrieves or creates a Payment record within a single atomic transaction.
        Additional fields can be provided via kwargs.
        """
        try:

            validator = PaymentValidator(document_number=document_number)
            if not validator.has_payment_fee():
                self.logger.warning(f"No payment fee required for document number: {document_number}")
                return None, False

            application = self._get_application(document_number=document_number)

            # Mandatory fields
            mandatory_fields = {
                'transaction_uuid': kwargs.get('transaction_uuid', uuid.uuid4().hex),
                'payment_date': kwargs.get('payment_date', date.today()),
                'status': kwargs.get('status', Payment.STATUS_PENDING),
                'description': kwargs.get('description', ''),
                'address': kwargs.get('address', ''),
                'full_name': application.full_name,
                'application_type': application.application_type
            }

            # Combine mandatory fields with provided kwargs
            defaults = {**mandatory_fields, **kwargs}

            payment, created = Payment.objects.get_or_create(
                reference_number=reference_number,
                document_number=document_number,
                amount=amount,
                defaults=defaults,
            )

            if created:
                self.logger.info(f"Created new payment for document number: {document_number}, "
                                 f"reference number: {reference_number}")
            else:
                self.logger.info(f"Retrieved existing payment for document number: {document_number}, "
                                 f"reference number: {reference_number}")

            return payment, created
        except Exception as e:
            self.logger.error(f"Transaction failed in get_or_create_payment for document number {document_number}: {e}")
            raise

    def _get_system_parameter(self, application_type):
        """
        Retrieves the SystemParameterPayment object for the given application type.
        """
        try:
            system_parameter = SystemParameterPayment.objects.get(application_type=application_type)
            self.logger.info(f"System parameter retrieved for application type: {application_type}")
            return system_parameter
        except SystemParameterPayment.DoesNotExist:
            self.logger.warning(f"No system parameter found for application type: {application_type}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving system parameter for application type {application_type}: {e}")
            raise

    @transaction.atomic
    def create(self, document_number, reference_number, application_type, **kwargs):
        """
        Creates a Payment record within a single atomic transaction.
        """
        try:
            system_parameter = self._get_system_parameter(application_type=application_type)
            if not system_parameter:
                self.logger.warning(f"Cannot create payment, system parameter missing for application type: "
                                    f"{application_type}")
                return None

            amount = system_parameter.amount
            payment, created = self.get_or_create_payment(
                document_number=document_number,
                amount=amount,
                reference_number=reference_number,
                **kwargs
            )
            if created:
                self.logger.info(f"Payment successfully created for document number: {document_number}")
            else:
                self.logger.info(f"Payment already exists for document number: {document_number}")
            return payment
        except Exception as e:
            self.logger.error(f"Transaction failed in create method for document number {document_number}: {e}")
            raise

    def _get_application(self, document_number):
        try:
            return Application.objects.get(
                application_document__document_number=document_number
            )
        except Application.DoesNotExist:
            return None

