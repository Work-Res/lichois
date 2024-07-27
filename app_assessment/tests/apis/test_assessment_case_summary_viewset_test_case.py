from django.test import TestCase, override_settings,  modify_settings
from django.conf import settings

from django.urls import reverse
from rest_framework import status
from app_assessment.models import AssessmentCaseSummary

from .base_test_api import BaseTestAPI


class AssessmentCaseSummaryViewSetTestCase(BaseTestAPI):

    def setUp(self):
        self.create_url = reverse('assessmentcasesummary-list')  # Assuming the viewset is registered with this name
        self.save_url = reverse('assessmentcasesummary-save_summary')

        # Create initial test data
        self.case_summary_data = {
            'parent_object_id': 'e8e8e8e8-e8e8-e8e8-e8e8-e8e8e8e8e8e8',
            'parent_object_type': 'app.Application',
            'summary': 'Initial summary',
            'data': {'key': 'value'},
            'document_number': 'DOC1234'  # Assuming this field is necessary
        }
        self.case_summary = AssessmentCaseSummary.objects.create(**self.case_summary_data)

    @override_settings(
        REST_FRAMEWORK={
            "DEFAULT_FILTER_BACKENDS": [
                "django_filters.rest_framework.DjangoFilterBackend",
                "rest_framework.filters.OrderingFilter",
            ],
            "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
            "DEFAULT_AUTHENTICATION_CLASSES": (),
        }
    )
    def test_create_valid(self):
        new_case_summary_data = {
            'parent_object_id': 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3d4e5f6',
            'parent_object_type': 'app.AnotherParentModel',
            'summary': 'New summary',
            'data': {'new_key': 'new_value'},
            'document_number': 'DOC5678'  # Assuming this field is necessary
        }

        response = self.client.post(self.create_url, new_case_summary_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssessmentCaseSummary.objects.count(), 2)
        self.assertEqual(AssessmentCaseSummary.objects.get(document_number='DOC5678').summary, 'New summary')

    def test_create_valid_when_parent_object_noavaliable(self):
        new_case_summary_data = {
            'summary': 'New summary',
            'document_number': 'DOC5678'  # Assuming this field is necessary
        }

        response = self.client.post(self.create_url, new_case_summary_data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssessmentCaseSummary.objects.count(), 2)
        self.assertEqual(AssessmentCaseSummary.objects.get(document_number='DOC5678').summary, 'New summary')

    def test_create_invalid(self):
        invalid_case_summary_data = {
            'parent_object_id': 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3d4e5f6',
            'parent_object_type': '',  # Invalid because it's blank
            'summary': 'New summary',
            'data': {'new_key': 'new_value'},
            'document_number': 'DOC5678'  # Assuming this field is necessary
        }

        response = self.client.post(self.create_url, invalid_case_summary_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AssessmentCaseSummary.objects.count(), 1)  # No new record should be created

    def test_save_valid(self):
        updated_case_summary_data = {
            'parent_object_id': self.case_summary.parent_object_id,
            'parent_object_type': self.case_summary.parent_object_type,
            'summary': 'Updated summary',
            'data': {'updated_key': 'updated_value'},
            'document_number': self.case_summary.document_number
        }

        response = self.client.post(self.save_url, updated_case_summary_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_case_summary = AssessmentCaseSummary.objects.get(document_number=self.case_summary.document_number)
        self.assertEqual(updated_case_summary.summary, 'Updated summary')

    def test_save_invalid(self):
        invalid_update_data = {
            'parent_object_id': self.case_summary.parent_object_id,
            'parent_object_type': '',  # Invalid because it's blank
            'summary': 'Updated summary',
            'data': {'updated_key': 'updated_value'},
            'document_number': self.case_summary.document_number
        }

        response = self.client.post(self.save_url, invalid_update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(
            AssessmentCaseSummary.objects.get(document_number=self.case_summary.document_number).summary,
            'Updated summary')
