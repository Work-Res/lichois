
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from authentication.models import User
from gazette.models import Batch
from gazette.models.batch_decision import BatchDecision


class BatchDecisionViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.batch = Batch.objects.create(title='Test Batch', description='Test Description')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_not_create_batch_decision(self):
        url = reverse('batch-decision-list')
        data = {'batch_id': self.batch.id, 'decision': 'APPROVED', 'comments': 'All good'}
        response = self.client.post(url, data, format='json')
        print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BatchDecision.objects.count(), 0)

    def test_should_create_batch_decision(self):
        url = reverse('batch-decision-list')
        self.batch.status = 'RECOMMENDED'
        self.batch.save()
        data = {'batch_id': self.batch.id, 'decision': 'APPROVED', 'comments': 'All good'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BatchDecision.objects.count(), 1)

    def test_retrieve_batch_decision(self):
        decision = BatchDecision.objects.create(batch=self.batch, decision='APPROVED')
        url = reverse('batch-decision-detail', args=[decision.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], 'APPROVED')
