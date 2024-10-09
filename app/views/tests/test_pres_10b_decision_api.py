"""
Test President Decision for 10B api
"""
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from app.api import NewApplicationDTO
from app.utils import ApplicationStatusEnum, ApplicationDecisionEnum

from app.classes import ApplicationService
from app.api.serializers.pres_recommendation_decision_serializer import PresRecommendationDecisionSerializer

from app.models import Application, ApplicationStatus
from citizenship.utils.citizenship_process_enum import CitizenshipProcessEnum
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from app.models import PresRecommendationDecision, ApplicationDecisionType
from app.tests.data import statuses
from citizenship.tests.base_setup import BaseSetup

PRES_DECISION_URL = reverse('pres-recommendation-decision-list')

def create_pres_decision(document_number, **params):

    defaults= {
        'date_approved': datetime.now(),
        'status': ApplicationDecisionType.objects.get(name='Accepted') ,
        'approved_by': 'TEST',
        'role':'TEST'
    }

    defaults.update(**params)

    decision = PresRecommendationDecision.objects.create(document_number=document_number, **defaults)
    return decision


def detail_url(decision_id):
    """Create and return a  detail URL."""
    return reverse('pres-recommendation-decision-detail', args=[decision_id])


class PublicPresDecision10BTests(BaseSetup):
    """Tests fot unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Tests for authentication required."""
        res = self.client.get(PRES_DECISION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePresDecision10BTests(BaseSetup):
    """Tests for authenticated users"""
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword')

        self.client.force_authenticate(self.user)

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def test_retrieve_decision(self):
        """Test retrieve Pres Recommendation Decision"""

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        create_pres_decision(role="PRESIDENT", document_number=app.application_document.document_number)

        res = self.client.get(PRES_DECISION_URL)

        decisions = PresRecommendationDecision.objects.all().order_by('-id')
        serializer = PresRecommendationDecisionSerializer(decisions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(decisions.count(), 1)

    def test_retrieve_decision_without_document_number(self):
        """Test retrieve Pres Recommendation Decision without document number"""
        res = self.client.get(PRES_DECISION_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"detail": "Document number is required"})



    def test_create_pres_decision(self):
        """Test creating a Pres Recommendation Decision"""

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        payload = {
            'document_number': app.application_document.document_number,
            'status': ApplicationDecisionEnum.ACCEPTED.value,
            'approved_by': 'TEST_USER',
            'role': 'PRESIDENT'
        }
        res = self.client.post(PRES_DECISION_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        decision = PresRecommendationDecision.objects.get(document_number=app.application_document.document_number)
        serializer = PresRecommendationDecisionSerializer(decision, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(decision.count(), 1)
        self.assertEqual(decision.status, ApplicationDecisionEnum.ACCEPTED.value)

    def test_create_pres_decision_invalid_data(self):
        """Test creating a Pres Recommendation Decision with invalid data"""
        payload = {
            'document_number': '',  # Invalid document number
            'status': ApplicationDecisionEnum.ACCEPTED.value,
            'approved_by': 'TEST_USER',
            'role': 'PRESIDENT'
        }
        res = self.client.post(PRES_DECISION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
