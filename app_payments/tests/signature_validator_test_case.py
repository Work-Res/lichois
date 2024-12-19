from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from base64 import b64encode
from hashlib import sha256
import hmac

from app_payments.validator import SignatureValidator


class SignatureValidatorTestCase(TestCase):
    def setUp(self):
        """
        Sets up common test data and configuration.
        """
        self.secret_key = "test_secret_key"
        self.valid_response_data = {
            "signed_field_names": "field1,field2,field3",
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
        }
        self.invalid_response_data = {
            "signed_field_names": "field1,field2",
            "field1": "value1",
            "field2": "value2",
        }

        # Add the computed valid signature
        self.valid_response_data["signature"] = self._generate_test_signature(
            self.valid_response_data
        )

        # Add a mismatched signature to the invalid data
        self.invalid_response_data["signature"] = "invalid_signature"

    def _generate_test_signature(self, response_data):
        """
        Generate a test signature based on the response data and secret key.
        """
        signed_field_names = response_data["signed_field_names"]
        fields_to_sign = [
            f"{field}={response_data[field]}" for field in signed_field_names.split(",")
        ]
        message_to_sign = ",".join(fields_to_sign)

        key = self.secret_key.encode("utf-8")
        message = message_to_sign.encode("utf-8")
        digest = hmac.new(key, msg=message, digestmod=sha256).digest()
        return b64encode(digest).decode("utf-8")

    def test_validate_with_valid_signature(self):
        """
        Tests validation with a valid signature.
        """
        try:
            settings.CYBERSOURCE_SECRET_KEY = self.secret_key
            SignatureValidator.validate(self.valid_response_data)
        except ValidationError:
            self.fail("validate() raised ValidationError unexpectedly!")

    def test_validate_with_invalid_signature(self):
        """
        Tests validation with an invalid signature.
        """
        error_value = None
        with self.assertRaises(ValidationError) as context:
            settings.CYBERSOURCE_SECRET_KEY = self.secret_key
            SignatureValidator.validate(self.invalid_response_data)
            error_value = context.exception[0] if len(context.exception) > 0 else ''
            self.assertEqual(error_value, "Invalid response signature.")

    def test_validate_missing_signed_field_names(self):
        """
        Tests validation when 'signed_field_names' is missing.
        """
        response_data = {
            "field1": "value1",
            "signature": "some_signature",
        }
        with self.assertRaises(ValidationError) as context:
            SignatureValidator.validate(response_data)
        self.assertEqual(context.exception.messages[0], "Missing required signature fields in the response.")

    def test_validate_missing_signature(self):
        """
        Tests validation when 'signature' is missing.
        """
        response_data = {
            "signed_field_names": "field1,field2",
            "field1": "value1",
        }
        with self.assertRaises(ValidationError) as context:
            SignatureValidator.validate(response_data)
        self.assertEqual(context.exception.messages[0], "Missing required signature fields in the response.")

    def test_secure_compare_equal_strings(self):
        """
        Tests secure comparison of two identical strings.
        """
        result = SignatureValidator._secure_compare("test123", "test123")
        self.assertTrue(result)

    def test_secure_compare_different_strings(self):
        """
        Tests secure comparison of two different strings.
        """
        result = SignatureValidator._secure_compare("test123", "test456")
        self.assertFalse(result)

