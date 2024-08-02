from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from authentication.models import User
from .base_setup import BaseSetup

from django.utils import timezone
from app_checklist.models import Region
from citizenship.models import Board, Role, Meeting


class MeetingViewSetTestCase(BaseSetup):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

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

    def test_create_meeting(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('citizenship:meeting-list')
        response = self.client.post(url, {
            'title': 'New Meeting',
            'board': self.board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-01T14:30:00+0000",
            'end_date': "2024-08-01T14:30:00+0000",
            'time': '11:00:00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_meetings(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('citizenship:meeting-list')
        response = self.client.post(url, {
            'title': 'New Meeting',
            'board': self.board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-01T14:30:00+0000",
            'end_date': "2024-08-01T14:30:00+0000",
            'time': '11:00:00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_meetings(self):
        self.meeting1 = Meeting.objects.create(
            title="Meeting 1",
            date=timezone.now().date(),
            time=timezone.now().time(),
            location="Location 1",
            agenda="Agenda 1",
            board=self.board,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(hours=2)
        )
        self.meeting2 = Meeting.objects.create(
            title="Meeting 2",
            date=timezone.now().date(),
            time=timezone.now().time(),
            location="Location 2",
            agenda="Agenda 2",
            board=self.board,
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=1, hours=2)
        )
        url = reverse('citizenship:meeting-list')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)


    def test_get_meetings_1(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('citizenship:meeting-list')
        response = self.client.post(url, {
            'title': 'New Meeting 1',
            'board': self.board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-01T14:30:00+0000",
            'end_date': "2024-08-01T14:30:00+0000",
            'time': '11:00:00'
        })

        response_1 = self.client.post(url, {
            'title': 'New Meeting 2',
            'board': self.board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-02T14:30:00+0000",
            'end_date': "2024-08-02T14:30:00+0000",
            'time': '11:00:00'
        })

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)

    def test_add_attendee(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/api/meetings/{self.meeting.id}/add_attendee/', {
            'member_id': self.user.id,
            'confirmed': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
