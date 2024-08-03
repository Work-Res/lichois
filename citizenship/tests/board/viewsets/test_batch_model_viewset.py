from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from django.urls import reverse

from authentication.models import User
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from citizenship.service.board import BatchService
from app_checklist.models import Region
from citizenship.models import Board, Role, Meeting, BoardMember, Batch, MeetingSession, BatchApplication, Attendee, \
    ConflictOfInterest

from .base_setup import BaseSetup


class BatchModelViewSetTest(BaseSetup):

    def setUp(self):
        super(BatchModelViewSetTest, self).setUp()
        self.region = Region.objects.create(
            name='Test Region',
            code='TR01',
            description='A test region',
            valid_from=timezone.now().date(),
            valid_to=(timezone.now() + timezone.timedelta(days=365)).date(),
            active=True
        )

        self.role1 = Role.objects.create(name='Role 1', description='First role')
        self.role2 = Role.objects.create(name='Role 2', description='Second role')

        self.board = Board.objects.create(
            name='Test Board',
            region=self.region,
            description='A test board'
        )
        self.board.quorum_roles.set([self.role1, self.role2])
        self.board.save()

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.role1 = Role.objects.create(name='Role 1', description='First role')
        self.member = BoardMember.objects.create(user=self.user, board=self.board, role=self.role1)

        self.client.login(username='testuser', password='testpass')
        url = reverse('citizenship:meeting-list')
        self.client.post(url, {
            'title': 'New Meeting',
            'board': self.board.id,
            'location': 'New Location',
            'agenda': 'New Agenda',
            'start_date': "2024-08-01T14:30:00+0000",
            'end_date': "2024-08-01T14:30:00+0000",
            'time': '11:00:00'
        })
        self.meeting = Meeting.objects.all().first()

    def test_create_batch(self):
        url = reverse('citizenship:batch-list')
        data = {
            'meeting': self.meeting.id,
            'name': 'New Test Batch'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Batch.objects.count(), 1)
        self.assertEqual(Batch.objects.latest('id').name, 'New Test Batch')

    def test_add_application(self):
        url = reverse('citizenship:meeting-create-session', args=[self.meeting.id])
        data = {
            'title': 'Morning Session',
            'date': timezone.now().date().isoformat(),
            'start_time': '11:00:00',
            'end_time':  '12:00:00'
        }
        self.client.post(url, data, format='json')
        meeting_sessing = MeetingSession.objects.get(meeting=self.meeting)

        url = reverse('citizenship:batch-list')
        data = {
            'meeting': self.meeting.id,
            'name': 'New Test Batch'
        }
        self.client.post(url, data, format='json')
        batch = Batch.objects.first()
        url = reverse('citizenship:batch-add-application', args=[batch.id])
        data = {
            'document_number': self.application.application_document.document_number,
            'session_id': meeting_sessing.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_applications(self):
        url = reverse('citizenship:meeting-create-session', args=[self.meeting.id])
        data = {
            'title': 'Morning Session',
            'date': timezone.now().date().isoformat(),
            'start_time': '11:00:00',
            'end_time':  '12:00:00'
        }
        self.client.post(url, data, format='json')
        meeting_sessing = MeetingSession.objects.get(meeting=self.meeting)

        url = reverse('citizenship:batch-list')
        data = {
            'meeting': self.meeting.id,
            'name': 'New Test Batch'
        }
        self.client.post(url, data, format='json')
        batch = Batch.objects.first()
        url = reverse('citizenship:batch-add-application', args=[batch.id])
        data = {
            'document_number': self.application.application_document.document_number,
            'session_id': meeting_sessing.id
        }
        self.client.post(url, data, format='json')

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        version = self.create_new_application()

        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_sessing.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_application(self):
        url = reverse('citizenship:meeting-create-session', args=[self.meeting.id])
        data = {
            'title': 'Morning Session',
            'date': timezone.now().date().isoformat(),
            'start_time': '11:00:00',
            'end_time':  '12:00:00'
        }
        self.client.post(url, data, format='json')
        meeting_sessing = MeetingSession.objects.get(meeting=self.meeting)

        url = reverse('citizenship:batch-list')
        data = {
            'meeting': self.meeting.id,
            'name': 'New Test Batch'
        }
        self.client.post(url, data, format='json')
        batch = Batch.objects.first()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        version = self.create_new_application()
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_sessing.id
        }
        self.client.post(url, data, format='json')
        self.assertEqual(BatchApplication.objects.filter(batch=batch).count(), 2)
        url = reverse('citizenship:batch-remove-application', args=[batch.id])
        data = {
            'application_id': version.application.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_declare_no_conflict_for_all(self):
        url = reverse('citizenship:meeting-create-session', args=[self.meeting.id])
        data = {
            'title': 'Morning Session',
            'date': timezone.now().date().isoformat(),
            'start_time': '11:00:00',
            'end_time':  '12:00:00'
        }
        self.client.post(url, data, format='json')
        meeting_sessing = MeetingSession.objects.get(meeting=self.meeting)

        url = reverse('citizenship:batch-list')
        data = {
            'meeting': self.meeting.id,
            'name': 'New Test Batch'
        }
        self.client.post(url, data, format='json')
        batch = Batch.objects.first()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        version = self.create_new_application()
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_sessing.id
        }
        self.client.post(url, data, format='json')

        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        ConflictOfInterestDuration.objects.create(
            meeting_session=meeting_sessing,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )

        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        attendee = Attendee.objects.get(meeting=self.meeting, member=self.member)
        data = {
            'attendee_id': attendee.id,
            'meeting_session_id': meeting_sessing.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count = ConflictOfInterest.objects.filter(attendee=attendee, has_conflict=False).count()
        self.assertEqual(count, 2)

