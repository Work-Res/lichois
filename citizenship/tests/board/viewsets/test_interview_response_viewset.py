import json
from django.urls import reverse

from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from app_checklist.models import (
    SystemParameterMarkingKey,
)
from citizenship.models import (
    InterviewResponse,
    Interview,
    MeetingSession,
    ConflictOfInterest,
    BoardMember,
)
from citizenship.models.board.conflict_of_interest_duration import (
    ConflictOfInterestDuration,
)

from ....models.board.score_sheet import ScoreSheet
from citizenship.service.board.batch_status_enum import BatchStatus

from .base_setup import BaseSetup
from ....service.word import DocumentGenerationService


class InterviewResponseViewSetTestCase(BaseSetup):

    def setUp(self):
        super().setUp()
        self.region = self.create_region()
        self.board = self.create_board(self.region)
        self.user, self.member = self.create_user_and_member(
            self.board, role="Deputy", username="testuser", description="test"
        )
        self.police, self.member_police = self.create_user_and_member(
            self.board, role="Police", username="police", description="test"
        )
        self.client.login(username="testuser", password="testpass")
        self.meeting = self.create_meeting(self.board)
        self.meeting_session = self.create_meeting_session(self.meeting)
        SystemParameterMarkingKey.objects.create(
            code="student_marking_key",
            pass_mark_in_percent="70",
            total_marks="100",
            valid_from=timezone.now(),
            valid_to=timezone.now(),
        )

    def test_create_interview_responses_for_batch_applications(self):

        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )

        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")
        duration.status = "completed"
        duration.save()
        responses = InterviewResponse.objects.all().count()
        self.assertEqual(responses, 14)

    def test_create_interview_responses_for_batch_applications_with_multiple_board_members(
        self,
    ):
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )

        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")

        self.client = APIClient()
        # Force login the user
        self.client.force_login(self.police)
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")

        conflicts = ConflictOfInterest.objects.all()
        self.assertEqual(conflicts.count(), 4)

        duration.status = "completed"
        duration.save()
        responses = InterviewResponse.objects.all().count()
        self.assertEqual(responses, 28)

    def test_update_interview_responses_for_batch_applications(self):
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")
        duration.status = "completed"
        duration.save()
        interview_response = InterviewResponse.objects.first()

        url = reverse(
            "citizenship:interviewresponse-detail", kwargs={"pk": interview_response.id}
        )
        data = {
            "response": "Updated response",
            "score": 5,
            "additional_comments": "testing",
        }
        response = self.client.put(url, data, format="json")
        interview_response = InterviewResponse.objects.get(id=interview_response.id)
        interview_response.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(interview_response.response, "Updated response")
        self.assertEqual(interview_response.score, 5)
        self.assertTrue(interview_response.is_marked)

    def test_bulk_update_successful(self):
        """Test bulk updating interview responses successfully."""
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")
        duration.status = "completed"
        duration.save()
        interview_responses = InterviewResponse.objects.all()

        url = reverse("citizenship:interviewresponse-bulk-update")
        bulk_data = [
            {
                "response_id": interview_responses[0].id,
                "data": {
                    "response": "Bulk Updated Response 1",
                    "score": 8,
                    "additional_comments": "bulk update test 1",
                },
            },
            {
                "response_id": interview_responses[1].id,
                "data": {
                    "response": "Bulk Updated Response 2",
                    "score": 7,
                    "additional_comments": "bulk update test 2",
                },
            },
        ]

        response = self.client.put(url, bulk_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        interview_responses[0].refresh_from_db()
        interview_responses[1].refresh_from_db()

        self.assertEqual(interview_responses[0].response, "Bulk Updated Response 1")
        self.assertEqual(interview_responses[1].response, "Bulk Updated Response 2")

    def test_bulk_update_with_nonexistent_ids(self):
        """Test bulk updating interview responses where some IDs do not exist."""
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")
        duration.status = "completed"
        duration.save()

        interview_response_first = InterviewResponse.objects.first()

        url = reverse("citizenship:interviewresponse-bulk-update")
        bulk_data = [
            {
                "response_id": 9999,  # Non-existent ID
                "data": {
                    "response": "Bulk Updated Response 1",
                    "score": 8,
                    "additional_comments": "bulk update test 1",
                },
            },
            {
                "response_id": interview_response_first.id,
                "data": {
                    "response": "Bulk Updated Response 2",
                    "score": 7,
                    "additional_comments": "bulk update test 2",
                },
            },
        ]

        response = self.client.put(url, bulk_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_update_by_member_successful(self):
        """Test bulk updating interview responses successfully."""
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")
        duration.status = "completed"
        duration.save()
        board_member = BoardMember.objects.get(user__username="testuser")
        interview = Interview.objects.first()

        interview_responses = InterviewResponse.objects.filter(
            member=board_member, interview=interview
        )

        url = reverse("citizenship:interviewresponse-bulk-update")
        bulk_data = [
            {
                "response_id": interview_responses[0].id,
                "data": {
                    "response": "Bulk Updated Response 1",
                    "score": 8,
                    "additional_comments": "bulk update test 1",
                },
            },
            {
                "response_id": interview_responses[1].id,
                "data": {
                    "response": "Bulk Updated Response 2",
                    "score": 7,
                    "additional_comments": "bulk update test 2",
                },
            },
            {
                "response_id": interview_responses[2].id,
                "data": {
                    "response": "Bulk Updated Response 3",
                    "score": 7,
                    "additional_comments": "bulk update test 3",
                },
            },
            {
                "response_id": interview_responses[3].id,
                "data": {
                    "response": "Bulk Updated Response 4",
                    "score": 20,
                    "additional_comments": "bulk update test 4",
                },
            },
            {
                "response_id": interview_responses[4].id,
                "data": {
                    "response": "Bulk Updated Response 5",
                    "score": 20,
                    "additional_comments": "bulk update test 5",
                },
            },
            {
                "response_id": interview_responses[5].id,
                "data": {
                    "response": "Bulk Updated Response 6",
                    "score": 15,
                    "additional_comments": "bulk update test 6",
                },
            },
            {
                "response_id": interview_responses[6].id,
                "data": {
                    "response": "Bulk Updated Response 7",
                    "score": 10,
                    "additional_comments": "bulk update test 7",
                },
            },
        ]

        response = self.client.put(url, bulk_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        interview_responses[0].refresh_from_db()
        interview_responses[1].refresh_from_db()

        self.assertEqual(interview_responses[0].response, "Bulk Updated Response 1")
        self.assertEqual(interview_responses[0].score, 8)
        self.assertEqual(interview_responses[1].response, "Bulk Updated Response 2")
        self.assertEqual(interview_responses[1].score, 7)
        self.assertEqual(interview_responses[2].response, "Bulk Updated Response 3")
        self.assertEqual(interview_responses[2].score, 7)
        self.assertEqual(interview_responses[3].response, "Bulk Updated Response 4")
        self.assertEqual(interview_responses[3].score, 20)
        self.assertEqual(interview_responses[4].response, "Bulk Updated Response 5")
        self.assertEqual(interview_responses[4].score, 20)
        self.assertEqual(interview_responses[5].response, "Bulk Updated Response 6")
        self.assertEqual(interview_responses[5].score, 15)
        self.assertEqual(interview_responses[6].response, "Bulk Updated Response 7")
        self.assertEqual(interview_responses[6].score, 10)

    def test_close_interview(self):
        """Test bulk updating interview responses successfully."""
        batch = self.create_batch(self.meeting)
        version = self.create_new_application()
        url = reverse("citizenship:batch-add-applications", args=[batch.id])
        data = {
            "document_numbers": [
                self.application.application_document.document_number,
                version.application.application_document.document_number,
            ],
            "session_id": self.meeting_session.id,
        }
        self.client.post(url, data, format="json")

        url = reverse("citizenship:batch-change-status", args=[batch.id])
        data = {"new_status": BatchStatus.CLOSED.name}
        response = self.client.post(url, data, format="json")
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
            status="open",
        )
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")

        self.client.login(username="police", password="testpass")
        url = reverse("citizenship:batch-declare-no-conflict-for-all", args=[batch.id])
        data = {"meeting_session_id": self.meeting_session.id}
        self.client.post(url, data, format="json")

        duration.status = "completed"
        duration.save()
        board_member = BoardMember.objects.get(user__username="testuser")
        interview = Interview.objects.first()

        interview_responses = InterviewResponse.objects.filter(
            member=board_member, interview=interview
        )

        self.client.login(username="testuser", password="testpass")
        url = reverse("citizenship:interviewresponse-bulk-update")
        bulk_data = self.bulk_update_date(interview_responses)
        response = self.client.put(url, bulk_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        interview_responses_2 = InterviewResponse.objects.filter(
            member=self.member_police, interview=interview
        )

        self.client.login(username="police", password="testpass")
        url = reverse("citizenship:interviewresponse-bulk-update")
        bulk_data = self.bulk_update_date(interview_responses_2)
        response = self.client.put(url, bulk_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        interview_responses = InterviewResponse.objects.filter(
            member=board_member, interview=interview
        )
        self.check_submitted_interview_response(interview_responses)

        interview_responses_2 = InterviewResponse.objects.filter(
            member=self.member_police, interview=interview
        )

        self.check_submitted_interview_response(interview_responses_2)
        interview.conducted = True
        interview.status = "completed"
        interview.save()

        self.service = DocumentGenerationService()
        score_sheet = ScoreSheet.objects.get(interview=interview)
        self.assertEqual(score_sheet.passed, True)

        self.service = DocumentGenerationService()
        self.service.generate_scoresheet_document(score_sheet)
        self.assertTrue(self.scoresheet.document.endswith('.docx'))
        self.assertIsNotNone(self.scoresheet.document)

    def check_submitted_interview_response(self, interview_responses):
        self.assertEqual(interview_responses[0].response, "Bulk Updated Response 1")
        self.assertEqual(interview_responses[0].score, 8)
        self.assertEqual(interview_responses[1].response, "Bulk Updated Response 2")
        self.assertEqual(interview_responses[1].score, 7)
        self.assertEqual(interview_responses[2].response, "Bulk Updated Response 3")
        self.assertEqual(interview_responses[2].score, 7)
        self.assertEqual(interview_responses[3].response, "Bulk Updated Response 4")
        self.assertEqual(interview_responses[3].score, 20)
        self.assertEqual(interview_responses[4].response, "Bulk Updated Response 5")
        self.assertEqual(interview_responses[4].score, 20)
        self.assertEqual(interview_responses[5].response, "Bulk Updated Response 6")
        self.assertEqual(interview_responses[5].score, 15)
        self.assertEqual(interview_responses[6].response, "Bulk Updated Response 7")
        self.assertEqual(interview_responses[6].score, 10)

    def bulk_update_date(self, interview_responses):
        bulk_data = [
            {
                "response_id": interview_responses[0].id,
                "data": {
                    "response": "Bulk Updated Response 1",
                    "score": 8,
                    "additional_comments": "bulk update test 1",
                },
            },
            {
                "response_id": interview_responses[1].id,
                "data": {
                    "response": "Bulk Updated Response 2",
                    "score": 7,
                    "additional_comments": "bulk update test 2",
                },
            },
            {
                "response_id": interview_responses[2].id,
                "data": {
                    "response": "Bulk Updated Response 3",
                    "score": 7,
                    "additional_comments": "bulk update test 3",
                },
            },
            {
                "response_id": interview_responses[3].id,
                "data": {
                    "response": "Bulk Updated Response 4",
                    "score": 20,
                    "additional_comments": "bulk update test 4",
                },
            },
            {
                "response_id": interview_responses[4].id,
                "data": {
                    "response": "Bulk Updated Response 5",
                    "score": 20,
                    "additional_comments": "bulk update test 5",
                },
            },
            {
                "response_id": interview_responses[5].id,
                "data": {
                    "response": "Bulk Updated Response 6",
                    "score": 15,
                    "additional_comments": "bulk update test 6",
                },
            },
            {
                "response_id": interview_responses[6].id,
                "data": {
                    "response": "Bulk Updated Response 7",
                    "score": 10,
                    "additional_comments": "bulk update test 7",
                },
            },
        ]
        return bulk_data
