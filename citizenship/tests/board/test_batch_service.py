from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Application
from authentication.models import User

from citizenship.models.board import Meeting, BatchApplication, BoardMember, Board
from citizenship.service.board import BatchService
from citizenship.validators.board.application_eligibility_validator import ApplicationEligibilityValidator
from unittest.mock import patch
from datetime import date


class BatchServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.board = Board.objects.create(name='Board1', description='Test board')
        self.member = BoardMember.objects.create(user=self.user, board=self.board)
        self.meeting = Meeting.objects.create(
            title='Test Meeting', board=self.board, location='Conference Room',
            agenda='Discuss project updates', status='Scheduled')
        self.application1 = Application.objects.create(applicant_name='Applicant 1',
                                                       application_date=date(2023, 7, 19),
                                                       document_number='DOC123', status='Approved')
        self.application2 = Application.objects.create(applicant_name='Applicant 2',
                                                       application_date=date(2023, 7, 19),
                                                       document_number='DOC124', status='Pending')

    def test_create_batch(self):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        self.assertIsNotNone(batch.id)
        self.assertEqual(batch.name, 'Batch 1')
        self.assertEqual(batch.meeting, self.meeting)

    @patch.object(ApplicationEligibilityValidator, 'is_eligible', return_value=True)
    def test_add_application_to_batch(self, mock_is_eligible):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        result = BatchService.add_application_to_batch(batch_id=batch.id, document_number='DOC123')
        self.assertTrue(result)
        self.assertTrue(BatchApplication.objects.filter(batch=batch, application=self.application1).exists())

    @patch.object(ApplicationEligibilityValidator, 'is_eligible', return_value=False)
    def test_add_application_to_batch_invalid(self, mock_is_eligible):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        with self.assertRaises(ValidationError):
            BatchService.add_application_to_batch(batch_id=batch.id, document_number='DOC124')

    @patch.object(ApplicationEligibilityValidator, 'is_eligible', return_value=True)
    def test_add_applications_to_batch(self, mock_is_eligible):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        result = BatchService.add_applications_to_batch(batch_id=batch.id, document_numbers=['DOC123', 'DOC124'])
        self.assertTrue(result)
        self.assertTrue(BatchApplication.objects.filter(batch=batch, application=self.application1).exists())
        self.assertTrue(BatchApplication.objects.filter(batch=batch, application=self.application2).exists())

    @patch.object(ApplicationEligibilityValidator, 'is_eligible', return_value=False)
    def test_add_applications_to_batch_invalid(self, mock_is_eligible):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        with self.assertRaises(ValidationError):
            BatchService.add_applications_to_batch(batch_id=batch.id, document_numbers=['DOC123', 'DOC124'])

    def test_remove_application_from_batch(self):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        BatchService.add_application_to_batch(batch_id=batch.id, document_number='DOC123')
        result = BatchService.remove_application_from_batch(batch_id=batch.id, application_id=self.application1.id)
        self.assertTrue(result)
        self.assertFalse(BatchApplication.objects.filter(batch=batch, application=self.application1).exists())

    def test_remove_application_from_batch_invalid(self):
        batch = BatchService.create_batch(meeting_id=self.meeting.id, name='Batch 1')
        with self.assertRaises(ValidationError):
            BatchService.remove_application_from_batch(batch_id=batch.id, application_id=self.application1.id)
