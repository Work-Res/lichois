from django.urls import reverse
from rest_framework import status
from datetime import timedelta

from rest_framework.test import APIClient
from authentication.models import User
from citizenship.models import InterviewResponse, Interview, MeetingSession, ConflictOfInterest
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration

from django.utils import timezone
from app_checklist.models import Region
from citizenship.models import Board, Role, Meeting, BoardMember, Batch
from citizenship.service.board.batch_status_enum import BatchStatus

from .base_setup import BaseSetup


class InterviewResponseViewSetTestCase(BaseSetup):

    def setUp(self):
        super().setUp()
        self.region = self.create_region()
        self.board = self.create_board(self.region)
        self.user, self.member = self.create_user_and_member(
            self.board, role="Deputy", username="testuser", description="test")
        self.police, self.member_police = self.create_user_and_member(
            self.board, role="Police", username="police", description="test")
        self.client.login(username='testuser', password='testpass')
        self.meeting = self.create_meeting(self.board)
        self.meeting_session = self.create_meeting_session(self.meeting)

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

    def create_user_and_member(self, board, username="testuser", role="", description=""):
        user = User.objects.create_user(username=username, password='testpass')
        role = Role.objects.create(name=role, description=description)
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

    def test_create_interview_responses_for_batch_applications(self):

        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': self.meeting_session.id
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
        # Declare conflict of interest..
        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        duration = ConflictOfInterestDuration.objects.create(
            meeting_session=self.meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )

        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        data = {
            'meeting_session_id': self.meeting_session.id
        }
        self.client.post(url, data, format='json')
        duration.status = "completed"
        duration.save()
        responses = InterviewResponse.objects.all().count()
        self.assertEqual(responses, 14)

    def test_create_interview_responses_for_batch_applications_with_multiple_board_members(self):
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': self.meeting_session.id
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
        # Declare conflict of interest..
        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        duration = ConflictOfInterestDuration.objects.create(
            meeting_session=self.meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )

        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        data = {
            'meeting_session_id': self.meeting_session.id
        }
        self.client.post(url, data, format='json')

        self.client = APIClient()
        # Force login the user
        self.client.force_login(self.police)
        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        data = {
            'meeting_session_id': self.meeting_session.id
        }
        self.client.post(url, data, format='json')

        conflicts = ConflictOfInterest.objects.all()
        self.assertEqual(conflicts.count(), 4)

        duration.status = "completed"
        duration.save()
        responses = InterviewResponse.objects.all().count()
        self.assertEqual(responses, 28)

    def test_update_interview_responses_for_batch_applications(self):
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse('citizenship:batch-add-applications', args=[batch.id])
        data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': self.meeting_session.id
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

        # Declare conflict of interest..
        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        duration = ConflictOfInterestDuration.objects.create(
            meeting_session=self.meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )
        url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        data = {
            'meeting_session_id': self.meeting_session.id
        }
        self.client.post(url, data, format='json')
        duration.status = "completed"
        duration.save()
        interview_response = InterviewResponse.objects.first()

        url = reverse('citizenship:interviewresponse-detail', kwargs={'pk': interview_response.id})
        data = {
            'response': 'Updated response',
            'score': 5,
            'additional_comments': 'testing'
        }
        interview_response = InterviewResponse.objects.get(id=interview_response.id)
        response = self.client.put(url, data, format='json')
        interview_response.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(interview_response.response, 'Updated response')
        self.assertEqual(interview_response.score, 5)
        self.assertTrue(interview_response.is_marked)
