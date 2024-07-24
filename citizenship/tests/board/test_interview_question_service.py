import pytest
import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from app_checklist.models import Region
from citizenship.models import InterviewQuestion, Meeting, Board
from citizenship.service.board import InterviewQuestionService


class InterviewQuestionServiceTestCase(TestCase):

    def setUp(self):
        self.region = Region.objects.create(
            name='Test Region',
            code='TR01',
            description='A test region',
            valid_from=timezone.now().date(),
            valid_to=(timezone.now() + timezone.timedelta(days=365)).date(),
            active=True
        )

        # Create Board
        self.board = Board.objects.create(name='Test Board', region=self.region)

        # Create Meeting
        self.meeting = Meeting.objects.create(
            board=self.board,
            title='Test Meeting',
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(hours=2),
            time=datetime.time(9, 0)
        )

        # Create InterviewQuestion
        self.interview_question = InterviewQuestion.objects.create(
            meeting=self.meeting,
            text='What are your strengths?'
        )

    def test_create_interview_question(self):
        interview_question = InterviewQuestionService.create_interview_question(
            meeting_id=self.meeting.id,
            text='What is your greatest weakness?'
        )
        self.assertIsNotNone(interview_question)
        self.assertEqual(interview_question.text, 'What is your greatest weakness?')
        self.assertEqual(interview_question.meeting, self.meeting)

    def test_create_interview_question_with_invalid_meeting(self):
        with self.assertRaises(ValidationError):
            InterviewQuestionService.create_interview_question(
                meeting_id=999,
                text='What is your greatest weakness?'
            )

    def test_get_interview_question(self):
        interview_question = InterviewQuestionService.get_interview_question(self.interview_question.id)
        self.assertIsNotNone(interview_question)
        self.assertEqual(interview_question.text, 'What are your strengths?')

    def test_get_interview_question_invalid(self):
        with self.assertRaises(ValidationError):
            InterviewQuestionService.get_interview_question(999)

    def test_update_interview_question(self):
        updated_interview_question = InterviewQuestionService.update_interview_question(
            question_id=self.interview_question.id,
            text='Describe a challenge you faced.'
        )
        self.assertEqual(updated_interview_question.text, 'Describe a challenge you faced.')

    def test_update_interview_question_invalid(self):
        with self.assertRaises(ValidationError):
            InterviewQuestionService.update_interview_question(
                question_id=999,
                text='Describe a challenge you faced.'
            )
