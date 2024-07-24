import pytest

from django.core.exceptions import ValidationError
from unittest.mock import patch

from citizenship.models import Meeting, Batch, BatchApplication, Attendee, ConflictOfInterest, Interview

from citizenship.service.board import BatchService
from citizenship.service.board.batch_status_enum import BatchStatus
from citizenship.validators.board.application_eligibility_validator import ApplicationEligibilityValidator

from .base_setup import BaseSetup


class BatchServiceTestCase(BaseSetup):

    def test_create_batch(self):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='New Batch')
        self.assertIsNotNone(batch)
        self.assertEqual(batch.name, 'New Batch')
        self.assertEqual(batch.meeting, self.meeting)

    def test_create_batch_with_invalid_meeting(self):
        with self.assertRaises(ValidationError):
            BatchService.create_batch(meeting_id=999, name='New Batch')

    def test_add_application_to_batch(self):
        with patch.object(ApplicationEligibilityValidator, 'is_valid', return_value=True):
            result = BatchService.add_application_to_batch(
                batch_id=self.batch.id, document_number=self.application.document_number, session_id=self.session.id)
            self.assertTrue(result)
            self.assertTrue(BatchApplication.objects.filter(
                batch=self.batch, application=self.application, meeting_session=self.session).exists())

    def test_add_application_to_batch_invalid(self):
        with patch.object(ApplicationEligibilityValidator, 'is_valid', return_value=False):
            with self.assertRaises(ValidationError):
                BatchService.add_application_to_batch(
                    batch_id=self.batch.id, document_number=self.application.document_number, session_id=self.session.id)

    def test_remove_application_from_batch(self):
        BatchApplication.objects.create(batch=self.batch, application=self.application, meeting_session=self.session)
        result = BatchService.remove_application_from_batch(
            batch_id=self.batch.id, application_id=self.application.id)
        self.assertTrue(result)
        self.assertFalse(BatchApplication.objects.filter(
            batch=self.batch, application=self.application, meeting_session=self.session).exists())

    def test_declare_conflict_of_interest(self):
        attendee = Attendee.objects.create(meeting=self.meeting, member=self.member)
        conflict = BatchService.declare_conflict_of_interest(
            attendee_id=attendee.id, document_number=self.application.application_document.document_number,
            has_conflict=True)
        self.assertIsNotNone(conflict)
        self.assertEqual(conflict.attendee, attendee)
        self.assertEqual(conflict.application, self.application)
        self.assertTrue(conflict.has_conflict)

    def test_change_batch_status(self):
        with patch.object(ApplicationEligibilityValidator, 'is_valid', return_value=True):
            BatchService.add_application_to_batch(
                batch_id=self.batch.id, document_number=self.application.document_number, session_id=self.session.id)
            BatchService.change_batch_status(batch_id=self.batch.id, new_status=BatchStatus.CLOSED.name)
            self.batch.refresh_from_db()
            self.assertEqual(self.batch.status, BatchStatus.CLOSED.name)
            self.assertTrue(Interview.objects.filter(application=self.application).exists())

    def test_declare_no_conflict_for_all(self):
        BatchApplication.objects.create(batch=self.batch, application=self.application, meeting_session=self.session)
        attendee = Attendee.objects.create(meeting=self.meeting, member=self.member)
        result = BatchService.declare_no_conflict_for_all(attendee_id=attendee.id, batch_id=self.batch.id)
        self.assertTrue(result)
        self.assertTrue(ConflictOfInterest.objects.filter(
            attendee=attendee, application=self.application, has_conflict=False).exists())
