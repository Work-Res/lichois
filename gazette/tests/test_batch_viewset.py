from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User
from gazette.models import Batch, BatchApplication

from .base_setup import BaseSetup


class BatchViewSetTests(BaseSetup):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_batch(self):
        url = reverse('batch-list')
        data = {'title': 'Test Batch', 'description': 'Test Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Batch.objects.count(), 1)
        self.assertEqual(Batch.objects.get().title, 'Test Batch')

    def test_add_application(self):
        batch = Batch.objects.create(title='Test Batch', description='Test Description')
        url = reverse('add_application', args=[batch.id])
        data = {'application_id':  self.application.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(batch.batch_applications.count(), 1)

    def test_add_application(self):
        batch = Batch.objects.create(title='Test Batch', description='Test Description')
        url = reverse('add_application', args=[batch.id])
        data = {'application_id':  self.application.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(batch.batch_applications.count(), 1)

    def test_add_applications_to_batch(self):
        batch = Batch.objects.create(title='Test Batch', description='Test Description')
        version = self.create_new_application()
        app1 = version.application
        version2 = self.create_new_application()
        app2 = version2.application

        url = reverse('add_applications', args=[batch.id])
        data = {
            'application_ids': [str(app1.id), str(app2.id)]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BatchApplication.objects.filter(batch=batch).count(), 2)

    def test_remove_application(self):
        batch = Batch.objects.create(title='Test Batch', description='Test Description')
        version = self.create_new_application()
        app1 = version.application
        BatchApplication.objects.create(batch=batch, application=app1)
        url = reverse('remove_application', args=[batch.id])
        data = {'application_id':  app1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(batch.batch_applications.count(), 0)

    def test_submit_batch(self):
        batch = Batch.objects.create(title='Test Batch', description='Test Description')
        version = self.create_new_application()
        app1 = version.application
        version2 = self.create_new_application()
        app2 = version2.application
        url = reverse('add_applications', args=[batch.id])
        data = {
            'application_ids': [str(app1.id), str(app2.id)]
        }
        response = self.client.post(url, data, format='json')

        url = reverse('submit_batch_submission', args=[batch.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        batch.refresh_from_db()
        self.assertEqual(batch.status, 'RECOMMANDED')

