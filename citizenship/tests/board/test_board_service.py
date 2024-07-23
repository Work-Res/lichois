from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Application, ApplicationDocument
from citizenship.models.board import Meeting, Attendee, Role, Board, BoardMember
from django.contrib.auth.models import User
from datetime import date, time

from citizenship.models.board.meeting_session import MeetingSession
from citizenship.service.board import BatchService


class BatchServiceTest(TestCase):

    def setUp(self):
        # Setup initial data for tests
        self.board = BoardMember.objects.create(name="Test Board", description="Test Description")
        self.role = Role.objects.create(name="Test Role", description="Test Role Description")
        self.user = User.objects.create(username="testuser")
        self.member = BoardMember.objects.create(user=self.user, board=self.board, role=self.role)
        self.meeting = Meeting.objects.create(title="Test Meeting", board=self.board, location="Test Location",
                                              agenda="Test Agenda", start_date=date.today(), end_date=date.today())
        self.session = MeetingSession.objects.create(meeting=self.meeting, title="Morning Session", date=date.today(),
                                                     start_time=time(9, 0), end_time=time(11, 0))
        self.application_document = ApplicationDocument.objects.create(document_number="12345")
        self.application = Application.objects.create(application_document=self.application_document)
        self.attendee = Attendee.objects.create(meeting=self.meeting, member=self.member)

    def test_create_batch(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        self.assertIsNotNone(batch)
        self.assertEqual(batch.name, "Test Batch")

    def test_add_application_to_batch(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        result = BatchService.add_application_to_batch(batch.id, self.application_document.document_number,
                                                       self.session.id)
        self.assertTrue(result)

    def test_add_application_to_batch_with_invalid_batch(self):
        with self.assertRaises(ValidationError):
            BatchService.add_application_to_batch(9999, self.application_document.document_number, self.session.id)

    def test_add_application_to_batch_with_invalid_application(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        with self.assertRaises(ValidationError):
            BatchService.add_application_to_batch(batch.id, "invalid_document_number", self.session.id)

    def test_add_application_to_batch_with_invalid_session(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        with self.assertRaises(ValidationError):
            BatchService.add_application_to_batch(batch.id, self.application_document.document_number, 9999)

    def test_add_applications_to_batch(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        document_numbers = [self.application_document.document_number]
        result = BatchService.add_applications_to_batch(batch.id, document_numbers, self.session.id)
        self.assertTrue(result)

    def test_add_applications_to_batch_with_invalid_batch(self):
        document_numbers = [self.application_document.document_number]
        with self.assertRaises(ValidationError):
            BatchService.add_applications_to_batch(9999, document_numbers, self.session.id)

    def test_add_applications_to_batch_with_invalid_application(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        with self.assertRaises(ValidationError):
            BatchService.add_applications_to_batch(batch.id, ["invalid_document_number"], self.session.id)

    def test_add_applications_to_batch_with_invalid_session(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        document_numbers = [self.application_document.document_number]
        with self.assertRaises(ValidationError):
            BatchService.add_applications_to_batch(batch.id, document_numbers, 9999)

    def test_remove_application_from_batch(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        BatchService.add_application_to_batch(batch.id, self.application_document.document_number, self.session.id)
        result = BatchService.remove_application_from_batch(batch.id, self.application.id)
        self.assertTrue(result)

    def test_remove_application_from_batch_with_invalid_batch_application(self):
        with self.assertRaises(ValidationError):
            BatchService.remove_application_from_batch(9999, 9999)

    def test_declare_conflict_of_interest(self):
        conflict = BatchService.declare_conflict_of_interest(self.attendee.id,
                                                             self.application_document.document_number, True)
        self.assertIsNotNone(conflict)
        self.assertTrue(conflict.has_conflict)

    def test_declare_conflict_of_interest_with_invalid_attendee(self):
        with self.assertRaises(ValidationError):
            BatchService.declare_conflict_of_interest(9999, self.application_document.document_number, True)

    def test_declare_conflict_of_interest_with_invalid_application(self):
        with self.assertRaises(ValidationError):
            BatchService.declare_conflict_of_interest(self.attendee.id, "invalid_document_number", True)

    def test_declare_no_conflict_for_all(self):
        batch = BatchService.create_batch(self.meeting.id, "Test Batch")
        BatchService.add_application_to_batch(batch.id, self.application_document.document_number, self.session.id)
        result = BatchService.declare_no_conflict_for_all(self.attendee.id, batch.id)
        self.assertTrue(result)

    def test_declare_no_conflict_for_all_with_invalid_attendee(self):
        with self.assertRaises(ValidationError):
            BatchService.declare_no_conflict_for_all(9999, 9999)
