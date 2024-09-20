from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app_production.models import ProductionAttachmentDocument
from authentication.models import User


class TestProductionAttachmentDocumentViewSet(APITestCase):

    def setUp(self):
        User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        # Create a test document
        self.document = ProductionAttachmentDocument.objects.create(
            document_number='12345',
            pdf_document=SimpleUploadedFile("test_document.pdf", b"file_content")
        )

    def test_download_by_number_success(self):
        """Test downloading a document by document_number when it exists."""
        url = reverse('productionattachmentdocument-download-by-number', kwargs={'document_number': '12345'})
        response = self.client.get(url)
        print(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="test_document.pdf"')
        self.assertEqual(response.content, b"file_content")

    def test_download_by_number_not_found(self):
        """Test downloading a document by document_number when it does not exist."""
        url = reverse('productionattachmentdocument-download-by-number', kwargs={'document_number': '67890'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Document not found'})
