import arrow
import uuid
from django.test import tag
from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from datetime import date
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from ..models import BoardMeeting, InterestDeclaration, MeetingAttendee


@tag('int')
class InterestDeclarationAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='test_user',
            password='password123')

        self.board = mommy.make_recipe(
            'board.board',
            id=uuid.uuid4()

        )

        self.board_member = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board,
            user_id=1
        )

        self.board_member2 = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board,
            user_id=2
        )

        self.board_member3 = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board
        )

        self.board_meeting = mommy.make_recipe(
            'board.boardmeeting',
            id=uuid.uuid4(),
            board_id=self.board.id
        )

        self.agenda_item = mommy.make_recipe(
            'board.agendaitem',
            id=uuid.uuid4()
        )

        self.interest_declaration = mommy.make_recipe(
            'board.interestdeclaration',
            id=uuid.uuid4(),
            interest_description='this is definitely a paragraph',
            meeting_attendee=MeetingAttendee.objects.filter(meeting=self.board_meeting)[0],
            agenda_item=self.agenda_item
        )

    @tag('int1')
    def test_list(self):
        url = reverse('board:interest-declarations-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('int2')
    def test_create(self):

        board_meeting_data = {'meeting_attendee': MeetingAttendee.objects.filter(meeting=self.board_meeting)[1].id,
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

    @tag('int4')
    def test_update(self):
        interest_declaration_data = {'interest_description': 'Updated meeting1'}
        url = reverse('board:interest-declarations-detail',
                      kwargs={'pk': self.interest_declaration.id})

        response = self.client.patch(url, interest_declaration_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InterestDeclaration.objects.get(id=self.interest_declaration.id).interest_description,
                         'Updated meeting1')

    @tag('int5')
    def test_delete(self):
        interest_declaration = mommy.make_recipe(
            'board.interestdeclaration',
            interest_description='this is text',
            meeting_attendee=MeetingAttendee.objects.filter(meeting=self.board_meeting)[1]
        )

        url = reverse('board:interest-declarations-detail',
                      kwargs={'pk': interest_declaration.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InterestDeclaration.objects.filter(id=interest_declaration.id).exists())
