import pytest
from django.core.exceptions import ValidationError

from django.utils import timezone

from app_checklist.models import Region
from citizenship.models import InterviewResponse, Interview, InterviewQuestion, BoardMember, Board, Role
from authentication.models import User
from citizenship.service.board.interview_response_service import InterviewResponseService
from citizenship.tests.board.base_setup import BaseSetup


class InterviewResponseServiceTestCase(BaseSetup):

    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username='johndoe', password='password123')
        self.role1 = Role.objects.create(name='Role 1', description='First role')
        self.role2 = Role.objects.create(name='Role 2', description='Second role')
        # Create Region
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

        # Create BoardMember
        self.member = BoardMember.objects.create(user=self.user, board=self.board, role=self.role1)

        # Create Interview
        self.interview = Interview.objects.create(
            application_id=1,
            date=timezone.now(),
            status='Scheduled'
        )

        # Create InterviewQuestion
        self.interview_question = InterviewQuestion.objects.create(
            meeting=self.interview.meeting,
            text='What are your strengths?'
        )

        # Create InterviewResponse
        self.interview_response = InterviewResponse.objects.create(
            interview=self.interview,
            question=self.interview_question,
            member=self.member,
            response='My strengths are...',
            score=5
        )

    def test_create_interview_response(self):
        response = InterviewResponseService.create_interview_response(
            interview_id=self.interview.id,
            question_id=self.interview_question.id,
            member_id=self.member.id,
            response='I am very motivated.',
            score=4
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.response, 'I am very motivated.')
        self.assertEqual(response.score, 4)

    def test_create_interview_response_with_invalid_interview(self):
        with self.assertRaises(ValidationError):
            InterviewResponseService.create_interview_response(
                interview_id=999,
                question_id=self.interview_question.id,
                member_id=self.member.id,
                response='I am very motivated.',
                score=4
            )

    def test_get_interview_response(self):
        response = InterviewResponseService.get_interview_response(self.interview_response.id)
        self.assertIsNotNone(response)
        self.assertEqual(response.response, 'My strengths are...')

    def test_get_interview_response_invalid(self):
        with self.assertRaises(ValidationError):
            InterviewResponseService.get_interview_response(999)

    def test_update_interview_response(self):
        updated_response = InterviewResponseService.update_interview_response(
            response_id=self.interview_response.id,
            response='I am very disciplined.',
            score=5
        )
        self.assertEqual(updated_response.response, 'I am very disciplined.')
        self.assertEqual(updated_response.score, 5)
        self.assertTrue(updated_response.is_marked)

    def test_update_interview_response_invalid(self):
        with self.assertRaises(ValidationError):
            InterviewResponseService.update_interview_response(
                response_id=999,
                response='I am very disciplined.',
                score=5
            )

    def test_delete_interview_response(self):
        result = InterviewResponseService.delete_interview_response(self.interview_response.id)
        self.assertTrue(result)
        with self.assertRaises(ValidationError):
            InterviewResponseService.get_interview_response(self.interview_response.id)

    def test_delete_interview_response_invalid(self):
        with self.assertRaises(ValidationError):
            InterviewResponseService.delete_interview_response(999)

    def test_list_interview_responses(self):
        responses = InterviewResponseService.list_interview_responses(interview_id=self.interview.id)
        self.assertTrue(len(responses) > 0)

    def test_create_responses_for_questions(self):
        questions = [self.interview_question.id]
        members = [self.member.id]
        responses = InterviewResponseService.create_responses_for_questions(
            interview_id=self.interview.id,
            question_ids=questions,
            member_ids=members
        )
        self.assertTrue(len(responses) > 0)

    def test_delete_all_responses_for_member(self):
        result = InterviewResponseService.delete_all_responses_for_member(self.member.id)
        self.assertTrue(result)
        responses = InterviewResponseService.list_interview_responses(member_id=self.member.id)
        self.assertEqual(len(responses), 0)
