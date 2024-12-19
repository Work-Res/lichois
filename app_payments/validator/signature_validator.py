import hmac
from hashlib import sha256
from base64 import b64encode
from django.core.exceptions import ValidationError
from django.conf import settings


class SignatureValidator:
    """
    Validates the CyberSource response signature to ensure data integrity.
    """

    @staticmethod
    def validate(response_data):
        """
        Validates the signature of the response data.
        """
        signed_field_names = response_data.get('signed_field_names')
        signature = response_data.get('signature')
        if not signed_field_names or not signature:
            raise ValidationError("Missing required signature fields in the response.")

        fields_to_sign = [f"{field}={response_data[field]}" for field in signed_field_names.split(',')]
        message_to_sign = ','.join(fields_to_sign)

        computed_signature = SignatureValidator._generate_signature(message_to_sign)
        if not SignatureValidator._secure_compare(computed_signature, signature):
            raise ValidationError("Invalid response signature.")

    @staticmethod
    def _generate_signature(message):
        """
        Generates a signature using HMAC SHA-256 and the CyberSource secret key.
        """
        key = settings.CYBERSOURCE_SECRET_KEY.encode('utf-8')
        message = message.encode('utf-8')
        digest = hmac.new(key, msg=message, digestmod=sha256).digest()
        return b64encode(digest).decode('utf-8')

    @staticmethod
    def _secure_compare(a, b):
        """
        Securely compares two strings to prevent timing attacks.
        """
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0
