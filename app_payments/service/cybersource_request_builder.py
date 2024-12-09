from django.conf import settings

from app_payments.service import PaymentService, CyberSourceService
from app_payments.service import ApplicantPaymentDetailsService
from app_payments.utils import CurrencyCode


class CybersourceRequestBuilder:
    """
    Class responsible for building the request body for CyberSource.
    """

    def __init__(self, document_number):
        self.document_number = document_number

    def build_request(self):
        """
        Builds the CyberSource request body.
        """
        payment_service = PaymentService()
        payment = payment_service.get_payment_by_document_number(document_number=self.document_number)
        applicant_details = ApplicantPaymentDetailsService(self.document_number).get_details()

        fields = {
            'profile_id': settings.CYBERSOURCE_PROFILE_ID,
            'access_key': settings.CYBERSOURCE_ACCESS_KEY,
            'amount': str(payment.amount),
            'transaction_uuid': str(payment.transaction_uuid),
            'payment_method': 'card',
            'bill_to_postal_code': '0000',
            'bill_to_state': 'Central',
            'locale': 'en',
            'currency': CurrencyCode.BWP.value,
            'transaction_type': 'sale',
            'reference_number': self.document_number,
        }
        fields.update(applicant_details)
        return fields

    def to_payment_context(self, context):
        applicant_payment_context = self.build_request()
        signed_fields = CyberSourceService.sign_fields(
            fields=applicant_payment_context, context=context)
        return signed_fields
