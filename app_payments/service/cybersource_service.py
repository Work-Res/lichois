import datetime
from base64 import b64encode
from hashlib import sha256
import hmac
from django.conf import settings


class CyberSourceService:
    """
    Service class for handling CyberSource-related operations.
    """

    @staticmethod
    def create_sha256_signature(key, message):
        """
        Generates an HMAC SHA-256 signature for a given message with Base64 encoding.
        """
        digest = hmac.new(
            key.encode(),
            msg=message.encode(),
            digestmod=sha256,
        ).digest()
        return b64encode(digest).decode()

    @staticmethod
    def sign_fields(fields, context):
        """
        Signs the provided fields dictionary for CyberSource Secure Acceptance integration.
        """
        fields['signed_date_time'] = (
            str(datetime.datetime.utcnow().isoformat(timespec='seconds')) + 'Z'
        )
        signed_field_names = []
        data_to_sign = []

        # Add each field name to signed_field_names
        for key, value in fields.items():
            signed_field_names.append(key)

        # Add `unsigned_field_names` and `signed_field_names` to the fields
        signed_field_names.append('unsigned_field_names')
        fields['unsigned_field_names'] = ''
        signed_field_names.append('signed_field_names')
        fields['signed_field_names'] = ','.join(signed_field_names)

        # Prepare the data to be signed
        for key, value in fields.items():
            data_to_sign.append(f'{key}={value}')

        # Generate signature
        signature = CyberSourceService.create_sha256_signature(
            settings.CYBERSOURCE_SECRET_KEY,
            ','.join(data_to_sign),
        )

        context['fields'] = fields
        context['signature'] = signature
        context['url'] = settings.CYBERSOURCE_URL

        return context
