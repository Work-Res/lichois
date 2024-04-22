import arrow
from django.test import tag
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APIClient
from rest_framework import status
from ..models import BoardMeeting


@tag('bmv')
class BoardMeetingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.board = mommy.make_recipe(
            'board.board', )

        self.board_member1 = mommy.make_recipe(
            'board.boardmember',
            board=self.board)

        self.board_member2 = mommy.make_recipe(
            'board.boardmember',
            board=self.board)

        self.board_member3 = mommy.make_recipe(
            'board.boardmember',
            board=self.board)

        self.board_meeting1 = mommy.make_recipe(
            'board.boardmeeting',
            description='meeting1',
            board_id=self.board.id)

        self.board_meeting2 = mommy.make_recipe(
            'board.boardmeeting',
            description='meeting2',
            board_id=self.board.id
        )

    @tag('bmv11')
    def test_list(self):
        url = reverse('board:board-meetings-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('bmv2')
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

    @tag('bmv3')
    def test_retrieve(self):
        url = reverse('board:board-meetings-detail',
                      kwargs={'pk': self.board_meeting2.id})

        response = self.client.get(url)

        # response = self.client.get(f'/board-meetings/{self.board_meeting2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'meeting2')

    @tag('bmv4')
    def test_update(self):
        board_meeting_data = {'name': 'Updated meeting1'}
        url = reverse('board:board-meetings-detail',
                      kwargs={'pk': self.board_meeting1.id})

        response = self.client.patch(url, board_meeting_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # breakpoint()
        self.assertEqual(BoardMeeting.objects.get(id=self.board_meeting1.id).description, 'meeting1')

    @tag('bmv5')
    def test_delete(self):
        board_meeting3 = mommy.make_recipe(
            'board.boardmeeting',
            description='meeting3',
            board_id=self.board.id
        )

        url = reverse('board:board-meetings-detail',
                      kwargs={'pk': board_meeting3.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BoardMeeting.objects.filter(id=board_meeting3.id).exists())
