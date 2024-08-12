from rest_framework.test import APIClient

from django.urls import reverse

from app.models import Application
from app_checklist.models import Region
from authentication.models import User
from citizenship.models import BatchApplication, Batch, MeetingSession, Meeting, Board, Role, BoardMember
import uuid
from django.utils import timezone

from ..base_setup import BaseSetup


class BatchApplicationFilterTestCase(BaseSetup):

    def create_region(self):
        return Region.objects.create(
            name='Test Region',
            code='TR01',
            description='A test region',
            valid_from=timezone.now().date(),
            valid_to=(timezone.now() + timezone.timedelta(days=365)).date(),
            active=True
        )

    def create_board(self, region):
        role1 = Role.objects.create(name='Role 1', description='First role')
        role2 = Role.objects.create(name='Role 2', description='Second role')
        board = Board.objects.create(
            name='Test Board',
            region=region,
            description='A test board'
        )
        board.quorum_roles.set([role1, role2])
        board.save()
        return board

    def create_user_and_member(self, board):
        user = User.objects.create_user(username='testuser', password='testpass')
        role = Role.objects.create(name='Role 1', description='First role')
        member = BoardMember.objects.create(user=user, board=board, role=role)
        return user, member

    def create_meeting(self, board):
        url = reverse('citizenship:meeting-list')
        self.client.post(url, {
            'title': 'New Meeting',
            'board': board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-01T14:30:00+0000",
            'end_date': "2024-08-01T14:30:00+0000",
            'time': '11:00:00'
        })
        return Meeting.objects.first()

    def setUp(self):
        super().setUp()
        self.client = APIClient()

        self.region = self.create_region()
        self.board = self.create_board(self.region)
        self.user, self.member = self.create_user_and_member(self.board)
        self.client.login(username='testuser', password='testpass')
        self.meeting = self.create_meeting(self.board)

        self.meeting_session = MeetingSession.objects.create(
            meeting=self.meeting,
            title="Session 1",
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            batch_application_complete=False
        )
        self.batch = Batch.objects.create(meeting=self.meeting, name="Batch 1")
        # Create BatchApplication instance
        self.batch_application = BatchApplication.objects.create(
            batch=self.batch,
            application=self.application,
            meeting_session=self.meeting_session
        )

    def test_filter_batch_application_by_batch(self):
        url = reverse('citizenship:batchapplication-list')
        response = self.client.get(url, {'batch': str(self.batch.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_filter_batch_application_by_application(self):
        url = reverse('citizenship:batchapplication-list')
        response = self.client.get(url, {'application': str(self.application.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_filter_batch_application_by_meeting_session(self):
        url = reverse('citizenship:batchapplication-list')
        response = self.client.get(url, {'meeting_session': str(self.meeting_session.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_filter_batch_application_by_meeting(self):
        url = reverse('citizenship:batchapplication-list')
        print(str(self.meeting.id))
        print(url)
        response = self.client.get(url, {'meeting': str(self.meeting.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)
