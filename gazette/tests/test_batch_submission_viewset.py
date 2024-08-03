from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from gazette.models import Batch


class BatchSubmissionViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.batch = Batch.objects.create(title='Test Batch', description='Test Description', created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_submit_batch(self):
        url = reverse('submit_batch_submission', args=[self.batch.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.status, 'COMPLETED')

    def test_update_batch_status(self):
        url = reverse('update_batch_status_submission', args=[self.batch.id])
        data = {'status': 'REVIEWED'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.status, 'REVIEWED')