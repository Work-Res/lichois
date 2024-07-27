from django.urls import reverse
from rest_framework import status
from app_assessment.models import AssessmentCaseDecision, AssessmentCaseSummary
from app_assessment.api.dto import AssessmentCaseDecisionDTO
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService
from .base_test_api import BaseTestAPI


class AssessmentCaseDecisionAPIViewTestCase(BaseTestAPI):

    def setUp(self):
        self.create_case_summary_url = reverse('assessmentcasesummary-list')
        self.save_case_summary_url = reverse('assessmentcasesummary-save_summary')
        self.url = reverse('assessmentcasedecision')  # Ensure the URL name matches your urls.py configuration
        self.valid_payload = {
            'document_number': 'DOC12345',
            'decision': 'Approved',
            'remarks': 'All criteria met.',
            'assessor': 'John Doe'
        }
        self.invalid_payload = {
            'document_number': '',
            'decision': 'Approved',
            'remarks': 'All criteria met.',
            'assessor': 'John Doe'
        }
        self.create_application_statuses()

    def test_post_valid_data(self):
        self.application_version = self.create_new_application()
        document_number = self.application_version.application.application_document.document_number
        new_case_summary_data = {
            'summary': 'New new summary',
            'document_number': document_number  # Assuming this field is necessary
        }
        self.client.post(self.create_case_summary_url, new_case_summary_data, format='json')
        summary = AssessmentCaseSummary.objects.get(
            document_number=document_number
        )

        valid_payload = {
            'parent_object_id': summary.id,
            'parent_object_type': 'app_assessment.AssessmentCaseSummary',
            'document_number': document_number,
            'decision': 'recommended',
            'author': 'tsetsiba',
            'author_role': "assessment_officer"
        }

        response = self.client.post(self.url, data=valid_payload, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(AssessmentCaseDecision.objects.filter(document_number=document_number).exists())

    def test_post_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_server_error(self):
        # Simulate a scenario where an unexpected error occurs in the service
        service = AssessmentCaseDecisionService(assessment_case_decision_dto=AssessmentCaseDecisionDTO(**self.valid_payload))
        service.create = lambda: (_ for _ in ()).throw(Exception('Server error'))

        response = self.client.post(self.url, data=self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)