import json

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from citizenship.tests.base_setup import BaseSetup
from django.contrib.auth import get_user_model
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from citizenship.utils.citizenship_process_enum import CitizenshipProcessEnum
from app.utils import ApplicationStatusEnum
from app.models import Application



APPLICATIONS_URL = reverse('application-list')
class TestApplicationApi:

    """
        Test suite for applications.
    """


    # def setUp(self):
    #     self.client = APIClient()
    #     self.new_application = NewApplicationDTO(
    #         process_name='residentpermit', applicant_identifier='3171111', status='new')

    def test_application_status_endpoints(self, application_status_factory):
        '''
           Pull a list of application statues
        '''

        application_status_factory()
        application_status_endpoint = "/api/v1/applications"
        self.client = APIClient()
        response = self.client.get(application_status_endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 1


class PrivateApplicationOrderBy(BaseSetup):

    """Tests for authenticated users"""
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword')

        self.client.force_authenticate(self.user)


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

        self.new_application_dto2 = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            applicant_identifier='428019626',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            full_name="Test test 2",
            applicant_type="immigrant"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)

        self.application_service2 = ApplicationService(
            new_application_dto=self.new_application_dto2)

        self.application_service.create_application()
        self.application_service2.create_application()

    def test_list_applications_default_ordering(self):


        res = self.client.get(APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        applications = Application.objects.all()

        dates = [app.created for app in applications]

        self.assertEqual(dates, sorted(dates))  #


    def test_list_applications_descending_order(self):
        """Test that the applications are returned in descending order by created date."""
        url = APPLICATIONS_URL + '?sort_by=created&order=desc'
        res = self.client.get(url)
        results = res.data['results']

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        created_dates = [app['application_status']['created'] for app in results]

        self.assertEqual(created_dates, sorted(created_dates, reverse=True))

    def test_invalid_ordering_field(self):
        """
        Test that an invalid sorting field returns a 400 .
        """
        url = APPLICATIONS_URL + '?sort_by=invalid_field'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_order_value(self):
        """
        Test that an invalid order value returns a 400.
        """
        url = APPLICATIONS_URL + '?sort_by=created&order=invalid'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)