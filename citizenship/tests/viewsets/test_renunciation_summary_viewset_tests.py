from django.urls import reverse

from rest_framework import status

from authentication.models import User
from .base_setup import BaseSetup

from rest_framework.test import APIClient


class TestRenunciationSummaryViewSetTests(BaseSetup):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_renunciation_summary_with_valid_document_number(self):
        """
        Ensure we can get the renunciation summary for a valid document number.
        """
        # Create the URL
        url = reverse('citizenship:renunciation-summary', kwargs={'document_number': self.document_number})

        # Make the GET request
        response = self.client.get(url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)

    def test_get_renunciation_summary_with_invalid_document_number(self):
        """
        Ensure that an invalid document number returns appropriate response.
        """
        # Create the URL

        url = reverse('citizenship:renunciation-summary', kwargs={'document_number': "INVALIDDOC"})

        # Make the GET request
        response = self.client.get(url)

        # Assertions
        # Assuming the invalid document number causes a 404 or 400 depending on the logic in ApplicationSummary
        # Adjust the expected status code based on your actual implementation
        self.assertEqual(len(response.data), 0)

