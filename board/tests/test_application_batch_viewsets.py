import arrow
import uuid
from django.test import tag
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from ..models import ApplicationBatch
from .meeting_setup_common import CommonSetupTestCase


@tag('apb')
class BoardMeetingViewSetTestCase(CommonSetupTestCase):
    def setUp(self):
        self.client = APIClient()

        self.app1 = mommy.make_recipe(
            'app.application',
            id=uuid.uuid4()
        )

        self.app2 = mommy.make_recipe(
            'app.application',
            id=uuid.uuid4()
        )

        self.app3 = mommy.make_recipe(
            'app.application',
            id=uuid.uuid4()
        )

        self.app_batch = mommy.make_recipe(
            'board.applicationbatch',
            id=uuid.uuid4(),
            make_m2m=True,
            batch_type='TESTING'
        )

    @tag('apb1')
    def test_list(self):
        url = reverse('board:application-batches-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('apb2')
    def test_create(self):
        app_batch_data = {'batch_id': uuid.uuid4(),
                          'batch_type': 'TESTING',
                          'applications': [self.app1.id, self.app2.id, self.app3.id],
                          'batch_duration': timedelta(hours=2, minutes=30)}

        url = reverse('board:application-batches-list')

        response = self.client.post(url, app_batch_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(ApplicationBatch.objects.filter(batch_type='TESTING').exists())

    @tag('apb3')
    def test_retrieve(self):
        application_batch2 = mommy.make_recipe(
                'board.applicationbatch',
            id=uuid.uuid4(),
            make_m2m=True,
            batch_type='TESTING2')

        url = reverse('board:application-batches-detail',
                      kwargs={'pk': application_batch2.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_type'], 'TESTING2')

    @tag('apb4')
    def test_update(self):
        app_batch_data = {'batch_type': 'UPDATED TESTING2'}
        url = reverse('board:application-batches-detail',
                      kwargs={'pk': self.app_batch.id})

        response = self.client.patch(url, app_batch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ApplicationBatch.objects.get(
            id=self.app_batch.id).batch_type, 'UPDATED TESTING2')

    @tag('apb5')
    def test_delete(self):
        application_batch3 = mommy.make_recipe(
            'board.applicationbatch',
            id=uuid.uuid4(),
            make_m2m=True,
            batch_type='TESTING3')

        url = reverse('board:application-batches-detail',
                      kwargs={'pk': application_batch3.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ApplicationBatch.objects.filter(id=application_batch3.id).exists())
