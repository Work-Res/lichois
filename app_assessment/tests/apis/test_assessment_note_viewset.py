from django.urls import reverse
from rest_framework import status
from app_assessment.models import AssessmentCaseNote, AssessmentCaseSummary
from .base_test_api import BaseTestAPI


class AssessmentNoteViewSetTestCase(BaseTestAPI):

    def setUp(self):

        super().setUp()

        self.create_url = reverse('assessmentnote-list') # Adjust this to match the correct URL pattern
        self.notes_url = reverse('assessmentnote-get-notes')
        version = self.create_new_application()
        self.document_number = version.application.application_document.document_number

        # Create a valid case summary for testing
        self.case_summary = AssessmentCaseSummary.objects.create(
            document_number=self.document_number,
            parent_object_id=version.id,
            parent_object_type='app.applicationVersion',
            summary='Test summary'
        )

        self.valid_payload = {
            'document_number': self.document_number,
            'parent_object_id': self.case_summary.id,
            'parent_object_type': 'app_assessment.AssessmentCaseSummary',
            'note_text': 'This is a test note.',
            'note_type': 'NOTE'
        }

        self.invalid_payload = {
            'document_number': '',
            'parent_object_id': 'parent-id-123',
            'parent_object_type': 'parent.type',
            'note_text': 'This is a test note.'
        }

    def test_create_valid(self):
        response = self.client.post(self.create_url, data=self.valid_payload, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AssessmentCaseNote.objects.filter(document_number=self.document_number).exists())

    def test_create_invalid(self):
        response = self.client.post(self.create_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_due_to_missing_summary(self):
        # Ensure the case summary is not present
        self.case_summary.delete()
        response = self.client.post(self.create_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(AssessmentCaseNote.objects.filter(document_number=self.document_number).exists())

    def test_get_notes(self):
        AssessmentCaseNote.objects.create(**self.valid_payload)
        response = self.client.get(self.notes_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['document_number'], self.document_number)

    def test_update_valid(self):
        case_note = AssessmentCaseNote.objects.create(**self.valid_payload)
        update_payload = {
            'document_number': self.document_number,
            'parent_object_id': self.case_summary.id,
            'parent_object_type': 'app_assessment.AssessmentCaseSummary',
            'note_text': 'This is an updated test note.',
            'note_type': 'NOTE'
        }
        response = self.client.put(f"{self.create_url}{case_note.pk}/", data=update_payload, format='json')

        self.assertTrue(response.data.get('status'))

    def test_update_invalid(self):
        case_note = AssessmentCaseNote.objects.create(**self.valid_payload)
        update_payload = {
            'document_number': '',
            'parent_object_id': 'parent-id-123',
            'parent_object_type': 'parent.type',
            'note': 'This is an updated test note.'
        }
        response = self.client.put(f"{self.create_url}{case_note.pk}/", data=update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
