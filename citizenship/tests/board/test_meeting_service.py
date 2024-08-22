import pytest
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase

from app_checklist.models import Region
from authentication.models import User
from citizenship.models import BoardMember, Board, Role
from citizenship.service.board import MeetingService
from django.utils import timezone


class MeetingServiceTestCase(TestCase):

    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username='johndoe', password='password123')

        # Create Role
        self.role = Role.objects.create(name='Chairperson', description='Board Chairperson')

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
        self.member = BoardMember.objects.create(user=self.user, board=self.board, role=self.role)

        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(hours=2)

    def test_create_meeting(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )
        self.assertIsNotNone(meeting)
        self.assertEqual(meeting.title, 'Test Meeting')
        self.assertEqual(meeting.board, self.board)

    def test_create_meeting_with_conflict(self):
        MeetingService.create_meeting(
            title='Test Meeting 1',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )
        with self.assertRaises(ValidationError):
            MeetingService.create_meeting(
                title='Test Meeting 2',
                board=self.board.id,
                location='Conference Room',
                agenda='Discuss Q4 targets',
                start_date=self.start_date,
                end_date=self.end_date,
                time=datetime.time(9, 0)
            )

    def test_add_attendee(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )
        attendee = MeetingService.add_attendee(meeting=meeting, member_id=self.member.id)
        self.assertIsNotNone(attendee)
        self.assertEqual(attendee.member, self.member)

    def test_remove_attendee(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )

        MeetingService.add_attendee(meeting=meeting, member_id=self.member.id)
        result = MeetingService.remove_attendee(meeting_id=meeting.id, member_id=self.member.id)
        self.assertTrue(result)

    def test_confirm_attendance(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )
        updated_attendee = MeetingService.confirm_attendance(meeting_id=meeting.id, member_id=self.member.id, confirmed=True)
        self.assertTrue(updated_attendee.confirmed)

    def test_confirm_attendance_with_proposed_date(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board.id,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=self.start_date,
            end_date=self.end_date,
            time=datetime.time(9, 0)
        )
        proposed_date = self.start_date + timezone.timedelta(days=1)
        updated_attendee = MeetingService.confirm_attendance(
            meeting_id=meeting.id,
            member_id=self.member.id,
            proposed_date=proposed_date
        )
        self.assertFalse(updated_attendee.confirmed)
        self.assertEqual(updated_attendee.proposed_date, proposed_date)
