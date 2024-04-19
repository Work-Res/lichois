import pytest
import json

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

# from app.api import NewApplication

pytestmark = pytest.mark.django_db


class TestApplicationApi(APITestCase):

    """
        Test suite for applications.
    """


    # def setUp(self):
    #     self.client = APIClient()
    #     self.new_application = NewApplication(
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
