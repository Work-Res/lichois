from rest_framework import status
from django.urls import reverse

from citizenship.models import Interview, InterviewResponse
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APIClient

from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from citizenship.service.board.batch_status_enum import BatchStatus

from .base_setup import BaseSetup


class InterviewViewSetTests(BaseSetup):
    def setUp(self):
        super().setUp()

        # Create necessary entities
        self.region = self.create_region()
        self.board = self.create_board(self.region)
        self.user, self.member = self.create_user_and_member(
            self.board, role="Deputy", username="testuser", description="test")
        self.police, self.member_police = self.create_user_and_member(
            self.board, role="Police", username="police", description="test")

        # Login
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('citizenship:interview-update-by-application')

        # Create a meeting and meeting session
        self.meeting = self.create_meeting(self.board)
        self.meeting_session = self.create_meeting_session(self.meeting)

        # Create batch and add applications
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        add_applications_url = reverse('citizenship:batch-add-applications', args=[batch.id])
        add_applications_data = {
            'document_numbers': [
                self.application.application_document.document_number,
                version.application.application_document.document_number
            ],
            'session_id': self.meeting_session.id
        }
        self.client.post(add_applications_url, add_applications_data, format='json')

        # Change batch status to closed
        change_status_url = reverse('citizenship:batch-change-status', args=[batch.id])
        change_status_data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(change_status_url, change_status_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        batch.refresh_from_db()
        self.assertEqual(batch.status, BatchStatus.CLOSED.name)
        self.assertEqual(Interview.objects.all().count(), 2)

        # Declare conflict of interest
        start_time = timezone.now() - timedelta(hours=1)
        end_time = timezone.now() + timedelta(hours=1)
        duration = ConflictOfInterestDuration.objects.create(
            meeting_session=self.meeting_session,
            start_time=start_time,
            end_time=end_time,
            status='open'
        )
        declare_conflict_url = reverse('citizenship:batch-declare-no-conflict-for-all', args=[batch.id])
        declare_conflict_data = {'meeting_session_id': self.meeting_session.id}
        self.client.post(declare_conflict_url, declare_conflict_data, format='json')
        duration.status = "completed"
        duration.save()

        # Update date
        interview_responses = InterviewResponse.objects.all()
        for ir in interview_responses:
            ir.score = 5
            ir.is_marked = True
            ir.response = "Answered correctly."
            ir.save()

        # Define valid payload for testing
        self.valid_payload = {
            'application_id': self.application.id,
            'conducted': True,
            'status': 'completed'
        }

    def test_update_by_application_missing_application_id(self):
        self.url = reverse('citizenship:interview-update-by-application')
        response = self.client.post(self.url, data={'conducted': True, 'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Application ID is required.")

    def test_update_by_application_missing_conducted_or_status(self):
        response = self.client.post(self.url, data={'application_id': self.application.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Both conducted and status fields are required.")

    def test_update_by_application_success(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        interview = Interview.objects.get(application=self.application)
        self.assertEqual(interview.status, "completed")
        self.assertEqual(interview.conducted, True)

    def test_update_by_application_validation_error(self):
        # Simulate a validation error by providing invalid data
        invalid_payload = {
            'application_id': 'invalid_app_id',
            'conducted': True,
            'status': 'completed'
        }
        response = self.client.post(self.url, data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_by_application_unexpected_error(self):
        # Simulate an unexpected error by providing invalid data that causes an exception
        invalid_payload = {
            'application_id': 'app123',
            'conducted': 'invalid_value',  # Invalid boolean value
            'status': 'completed'
        }
        response = self.client.post(self.url, data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
