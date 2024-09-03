from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User
from gazette.models import LegalAssessment

from .base_setup import BaseSetup


class LegalAssessmentViewSetTests(BaseSetup):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_legal_assessment(self):
        url = reverse('legal-assessment-list')
        data = {'application_id': self.application.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LegalAssessment.objects.count(), 1)
        self.assertEqual(LegalAssessment.objects.get().assessment_text, 'Initial Assessment')

    def test_update_legal_assessment(self):
        assessment = LegalAssessment.objects.create(
            application=self.application, legal_member=self.user, assessment_text='Initial Assessment')
        url = reverse('legal-assessment-detail', args=[assessment.id])
        data = {'assessment_text': 'Updated Assessment'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assessment.refresh_from_db()
        self.assertEqual(assessment.assessment_text, 'Updated Assessment')

    def test_retrieve_legal_assessment(self):
        assessment = LegalAssessment.objects.create(
            application=self.application, legal_member=self.user, assessment_text='Initial Assessment')
        url = reverse('legal-assessment-detail', args=[assessment.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assessment_text'], 'Initial Assessment')

    def test_list_legal_assessments(self):
        url = reverse('legal-assessment-list')
        data = {'application_id': self.application.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')

        url = reverse('legal-assessment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_legal_assessments_should_raise_validation(self):
        url = reverse('legal-assessment-list')
        data = {'application_id': self.application.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')

        url = reverse('legal-assessment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse('legal-assessment-list')
        data = {'application_id': self.application.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(len(response.data), 1)

    def test_list_legal_assessments_create_multiple(self):
        url = reverse('legal-assessment-list')
        data = {'application_id': self.application.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')

        url = reverse('legal-assessment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        version = self.create_new_application()
        app = version.application
        url = reverse('legal-assessment-list')
        data = {'application_id': app.id, 'assessment_text': 'Initial Assessment'}
        response = self.client.post(url, data, format='json')
        legal_assessments = LegalAssessment.objects.all().count()
        self.assertEqual(legal_assessments, 2)
