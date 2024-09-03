from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from authentication.models import User
from gazette.models import Batch


class BatchSubmissionViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.batch = Batch.objects.create(title='Test Batch', description='Test Description')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_submit_batch(self):
        url = reverse('submit_batch_submission', args=[self.batch.id])
        response = self.client.post(url, format='json')
        print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.batch.refresh_from_db()
        # self.assertEqual(self.batch.status, '')

    def test_update_batch_status(self):
        url = reverse('update_batch_status_submission', args=[self.batch.id])
        data = {'status': 'REVIEWED'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.status, 'REVIEWED')
