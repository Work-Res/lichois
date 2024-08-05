from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from django.urls import reverse

from authentication.models import User
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from app_checklist.models import Region
from citizenship.models import Board, Role, Meeting, BoardMember, Batch, MeetingSession, BatchApplication, Attendee, \
    ConflictOfInterest, Interview, InterviewResponse
from citizenship.service.board.batch_status_enum import BatchStatus

from .base_setup import BaseSetup


class BatchModelViewSetTest(BaseSetup):

    def setUp(self):
        super(BatchModelViewSetTest, self).setUp()
        self.region = self.create_region()
        self.board = self.create_board(self.region)
        self.user, self.member = self.create_user_and_member(self.board)
        self.client.login(username='testuser', password='testpass')
        self.meeting = self.create_meeting(self.board)

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

    def create_meeting_session(self, meeting):
        url = reverse('citizenship:meeting-create-session', args=[meeting.id])
        data = {
            'title': 'Morning Session',
            'date': timezone.now().date().isoformat(),
            'start_time': '11:00:00',
            'end_time': '12:00:00'
        }
        self.client.post(url, data, format='json')
        return MeetingSession.objects.get(meeting=meeting)

    def create_batch(self, meeting):
        url = reverse('citizenship:batch-list')
        data = {
            'meeting': meeting.id,
            'name': 'New Test Batch'
        }
        self.client.post(url, data, format='json')
        return Batch.objects.first()

    def test_create_batch(self):
        batch = self.create_batch(self.meeting)
        self.assertIsNotNone(batch)
        self.assertEqual(batch.name, 'New Test Batch')

    def test_add_application(self):
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        url = reverse('citizenship:batch-add-application', args=[batch.id])
        data = {
            'document_number': self.application.application_document.document_number,
            'session_id': meeting_session.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_applications(self):
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_session.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_application(self):
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_session.id
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
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_session.id
        }
        self.client.post(url, data, format='json')

        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        ConflictOfInterestDuration.objects.create(
            meeting_session=meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )

        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        attendee = Attendee.objects.get(meeting=self.meeting, member=self.member)
        data = {
            'attendee_id': attendee.id,
            'meeting_session_id': meeting_session.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count = ConflictOfInterest.objects.filter(attendee=attendee, has_conflict=False).count()
        self.assertEqual(count, 2)

    def test_conflict_of_interest_when_completed(self):
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()

        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_session.id
        }
        self.client.post(url, data, format='json')

        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        conflict_of_interest_duration = ConflictOfInterestDuration.objects.create(
            meeting_session=meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )
        # close batch so that interview object get created.
        url = reverse('citizenship:batch-change-status', args=[batch.id])
        data = {
            "new_status": BatchStatus.CLOSED.name
        }
        self.client.post(url, data, format='json')

        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        attendee = Attendee.objects.get(meeting=self.meeting, member=self.member)
        data = {
            'attendee_id': attendee.id,
            'meeting_session_id': meeting_session.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count = ConflictOfInterest.objects.filter(attendee=attendee, has_conflict=False).count()
        self.assertEqual(count, 2)

        conflict_of_interest_duration.status = "completed"
        conflict_of_interest_duration.save()
        interview_responses = InterviewResponse.objects.all()
        self.assertEqual(interview_responses.count(), 14)

    def test_close_batch(self):
        batch = self.create_batch(self.meeting)
        url = reverse('citizenship:batch-change-status', args=[batch.id])
        data = {
            "new_status": BatchStatus.CLOSED.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        batch.refresh_from_db()
        self.assertEqual(batch.status, BatchStatus.CLOSED.name)

    def test_close_batch_when_batch_empty(self):
        batch = self.create_batch(self.meeting)
        url = reverse('citizenship:batch-change-status', args=[batch.id])
        data = {
            "new_status": BatchStatus.CLOSED.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        batch.refresh_from_db()
        self.assertEqual(batch.status, BatchStatus.CLOSED.name)

    def test_close_batch_when_batch_not_empty(self):
        meeting_session = self.create_meeting_session(self.meeting)
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': meeting_session.id
        }
        self.client.post(url, data, format='json')

        url = reverse('citizenship:batch-change-status', args=[batch.id])
        data = {
            "new_status": BatchStatus.CLOSED.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        batch.refresh_from_db()
        self.assertEqual(batch.status, BatchStatus.CLOSED.name)
        self.assertEqual(Interview.objects.all().count(), 2)

    def test_close_already_closed_batch(self):
        batch = self.create_batch(self.meeting)
        batch.status = BatchStatus.CLOSED.name
        batch.save()
        data = {
            "new_status": BatchStatus.CLOSED.name
        }
        
        url = reverse('citizenship:batch-change-status', args=[batch.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
