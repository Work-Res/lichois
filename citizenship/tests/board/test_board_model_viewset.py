import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from citizenship.management.factory.factories import RoleFactory, BoardFactory, BoardMemberFactory


from citizenship.models import Board


class TestBoardModelViewSet(APITestCase):

    def setUp(self):

        # Create Region
        # Use the factory to create a Board instance
        chair_person = RoleFactory(name='Chairperson')
        police_officer = RoleFactory(name='Police Officer')
        deputy_chair = RoleFactory(name='Deputy Chair')
        citizenship_officer = RoleFactory(name='Citizenship Officer')
        self.board = BoardFactory(
            quorum_roles=[chair_person, police_officer, deputy_chair, citizenship_officer])
        chair_person_member = BoardMemberFactory(board=self.board, role=chair_person)
        police_officer_member = BoardMemberFactory(board=self.board, role=police_officer)
        deputy_chair_member = BoardMemberFactory(board=self.board, role=deputy_chair)
        citizenship_officer = BoardMemberFactory(board=self.board, role=citizenship_officer)

        self.meeting_data = {
            'title': 'Board Meeting',
            'location': 'Gaborone',
            'agenda': 'Test Agenda',
            'status': 'draft',
            'start_date': datetime.date.today(),
            'end_date':  datetime.date.today(),
            'board': self.board.id
        }

    def test_add_meeting(self):
        create_meeting_url = reverse('meeting-list')
        response = self.client.post(create_meeting_url, self.meeting_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.meeting_data['title'])
        self.assertTrue(Board.objects.get(id=self.board.id).meetings.filter(title=self.meeting_data['title']).exists())
