from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from app.api import NewApplication


class TestApplicationApi(APITestCase):

    """
    Test suite for New Application
    """
    def setUp(self):
        self.client = APIClient()
        self.new_application = NewApplication(
            process_name='residentpermit', applicant_identifier='3171111', status='new')

    def test_create_new_application(self):
        '''
        test ContactViewSet create method
        '''
        pass
        # data = self.data
        # response = self.client.post(self.url, data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Contact.objects.count(), 1)
        # self.assertEqual(Contact.objects.get().title, "Billy Smith")
