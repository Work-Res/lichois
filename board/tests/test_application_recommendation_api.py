import arrow
import uuid
from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from ..models import ApplicationBatch
from .meeting_setup_common import CommonSetupTestCase


@tag('bm')
class BoardMeetingAPITests(CommonSetupTestCase, APITestCase):

    def setUp(self):
        super().setUp()

        # self.app1 = mommy.make_recipe(
        #     'app.application',
        #     id=uuid.uuid4()
        # )
        #
        # self.app2 = mommy.make_recipe(
        #     'app.application',
        #     id=uuid.uuid4()
        # )
        #
        # self.app3 = mommy.make_recipe(
        #     'app.application',
        #     id=uuid.uuid4()
        # )

        self.app_batch = mommy.make_recipe(
            'board.applicationbatch',
            id=uuid.uuid4(),
            make_m2m=True,
            batch_type='TESTING'
        )

        # self.app_batch.applications.add(self.app1, self.app2,
        #                                 self.app3)

    @tag('bm1')
    def test_get_board_decisions(self):
        url = reverse('board:board-decision-votes-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @tag('bm2')
    def test_retrieve(self):

        url = reverse('board:application-batches-detail',
                      kwargs={'pk': self.app_batch.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_type'], 'TESTING')

    @tag('bm3')
    def test_create(self):
        board_meeting_data = {'description': 'test meeting',
                              'meeting_date': arrow.utcnow().datetime,
                              'board_id': self.board.id,
                              'status': 'scheduled',
                              'meeting_type': 'physical',
                              'location': 'CBD'}

        url = reverse('board:board-meetings-list')

        response = self.client.post(url, board_meeting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BoardMeeting.objects.filter(description='test meeting').exists())

    @tag('bm4')
    def test_retrieve(self):
        url = reverse('board:application-batches-detail',
                      kwargs={'pk': self.app_batch.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_type'], 'TESTING')

