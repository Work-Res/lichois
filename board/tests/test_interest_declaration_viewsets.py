import arrow
from django.test import tag
from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from datetime import date
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from ..models import InterestDeclaration, MeetingAttendee


@tag('att')
class InterestDeclarationAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='test_user',
            password='password123')

        self.board = mommy.make_recipe(
            'board.board',
        )

        self.board_member = mommy.make_recipe(
            'board.boardmember',
            board=self.board
        )

        self.board_meeting = mommy.make_recipe(
            'board.boardmeeting',
            board_id=self.board.id
        )

        self.agenda_item = mommy.make_recipe(
            'board.agendaitem'
        )

        self.interest_declaration = mommy.make_recipe(
            'board.interestdeclaration',
            interest_description='this is definitely a paragraph',
            meeting_attendee=MeetingAttendee.objects.filter(meeting=self.board_meeting)[0],
            agenda_item=self.agenda_item
        )

    @tag('bmv1')
    def test_list(self):
        url = reverse('board:interest-declarations-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('bmv12')
    def test_create(self):

        board_meeting_data = {'meeting_attendee': MeetingAttendee.objects.filter(meeting=self.board_meeting)[0].id,
                              'agenda_item': self.agenda_item.id,
                              'board_id': self.board.id,
                              'client_relationship': 'investment',
                              'interest_description': 'this is a paragraph',
                              'decision': 'refrain',
                              'chair_person': self.board_member.id,
                              'attendee_signature': 'texttext',
                              'date_signed': date.today()}

        url = reverse('board:interest-declarations-list')

        response = self.client.post(url, board_meeting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(InterestDeclaration.objects.filter(interest_description='this is a paragraph').exists())

    @tag('bmv12')
    def test_retrieve(self):
        url = reverse('board:interest-declarations-detail',
                      kwargs={'pk': self.interest_declaration.id})

        response = self.client.get(url)

        # response = self.client.get(f'/board-meetings/{self.board_meeting2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['interest_description'], 'this is definitely a paragraph')

    @tag('bmv1')
    def test_update(self):
        board_meeting_data = {'name': 'Updated meeting1'}
        url = reverse('board:interest-declarations-detail',
                      kwargs={'pk': self.board_meeting1.id})

        response = self.client.patch(url, board_meeting_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BoardMeeting.objects.get(id=self.board_meeting1.id).description, 'meeting1')

    @tag('bmv1')
    def test_delete(self):
        board_meeting3 = mommy.make_recipe(
            'board.boardmeeting',
            description='meeting3',
            board_id=self.board.id
        )

        url = reverse('board:interest-declarations-detail',
                      kwargs={'pk': board_meeting3.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BoardMeeting.objects.filter(id=board_meeting3.id).exists())
