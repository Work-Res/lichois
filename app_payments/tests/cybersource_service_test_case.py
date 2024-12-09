from django.test import TestCase
from django.conf import settings

from hashlib import sha256
import hmac
from base64 import b64encode

from django.urls import reverse_lazy

from app_payments.service import CyberSourceService


class CyberSourceServiceTestCase(TestCase):
    def setUp(self):
        """
        Sets up common test data and configuration.
        """
        self.secret_key = "test_secret_key"
        self.fields = {
            "field1": "value1",
            "field2": "value2",
        }
        self.context = {}

    def _generate_test_signature(self, data_to_sign):
        """
        Generate a test signature based on the data to sign and secret key.
        """
        key = self.secret_key.encode("utf-8")
        message = data_to_sign.encode("utf-8")
        digest = hmac.new(key, msg=message, digestmod=sha256).digest()
        return b64encode(digest).decode("utf-8")

    def test_create_sha256_signature(self):
        """
        Tests the creation of an HMAC SHA-256 signature.
        """
        message = "field1=value1,field2=value2"
        expected_signature = self._generate_test_signature(message)
        actual_signature = CyberSourceService.create_sha256_signature(self.secret_key, message)
        self.assertEqual(expected_signature, actual_signature)

    def test_sign_fields(self):
        """
        Tests signing of fields for CyberSource integration.
        """
        settings.CYBERSOURCE_SECRET_KEY = self.secret_key
        signed_context = CyberSourceService.sign_fields(self.fields.copy(), self.context.copy())

        # Check if 'signed_date_time' is added
        self.assertIn('signed_date_time', signed_context['fields'])

        # Check if 'signed_field_names' is correctly populated
        signed_field_names = signed_context['fields']['signed_field_names'].split(',')
        for field in self.fields.keys():
            self.assertIn(field, signed_field_names)
        self.assertIn('signed_date_time', signed_field_names)
        self.assertIn('unsigned_field_names', signed_field_names)
        self.assertIn('signed_field_names', signed_field_names)

        # Check if 'unsigned_field_names' is set to an empty string
        self.assertEqual(signed_context['fields']['unsigned_field_names'], '')

        # Prepare data to sign
        data_to_sign = ','.join([f'{key}={signed_context["fields"][key]}' for key in signed_field_names])

        # Generate expected signature
        expected_signature = self._generate_test_signature(data_to_sign)

        # Check if the signature matches
        self.assertEqual(signed_context['signature'], expected_signature)

        # Check if the URL is set correctly
        self.assertEqual(signed_context['url'], settings.CYBERSOURCE_URL)

    def test_url(self):
        success_url = reverse_lazy("password_reset_done")
        print(">>>>>>>>>>>>>>", reverse_lazy("payment-response"))

