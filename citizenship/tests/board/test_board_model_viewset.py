from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.utils import timezone
from citizenship.models import Role

from app_checklist.models import Region
from citizenship.models import Board


class BoardModelViewSetTests(APITestCase):

    def setUp(self):

        # Create Region
        self.region = Region.objects.create(
            name='Test Region',
            code='TR01',
            description='A test region',
            valid_from=timezone.now().date(),
            valid_to=(timezone.now() + timezone.timedelta(days=365)).date(),
            active=True
        )

        # Create Roles
        self.role1 = Role.objects.create(name='Role 1', description='First role')
        self.role2 = Role.objects.create(name='Role 2', description='Second role')

        # Create Board
        self.board = Board.objects.create(
            name='Test Board',
            region=self.region,
            description='A test board'
        )
        self.board.quorum_roles.set([self.role1, self.role2])
        self.board.save()

        self.board_data = {
            'name': 'Test Board',
            'region_id': 1,
            'description': 'Test Description',
            'quorum_role_ids': [1, 2]
        }
        self.update_data = {
            'name': 'Updated Test Board',
            'region_id': 2,
            'description': 'Updated Description',
            'quorum_role_ids': [2, 3]
        }
        self.meeting_data = {
            'title': 'Test Meeting',
            'location': 'Test Location',
            'agenda': 'Test Agenda',
            'status': 'Scheduled'
        }

    def test_create_board(self):
        url = reverse('board-list')
        response = self.client.post(url, self.board_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.board_data['name'])
        self.assertTrue(Board.objects.filter(name=self.board_data['name']).exists())

    def test_update_board(self):
        board = Board.objects.create(**self.board_data)
        url = reverse('board-detail', args=[board.id])
        response = self.client.put(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.update_data['name'])
        board.refresh_from_db()
        self.assertEqual(board.name, self.update_data['name'])

    def test_add_meeting(self):
        board = Board.objects.create(**self.board_data)
        url = reverse('board-add-meeting', args=[board.id])
        response = self.client.post(url, self.meeting_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.meeting_data['title'])
        self.assertTrue(Board.objects.get(id=board.id).meetings.filter(title=self.meeting_data['title']).exists())
