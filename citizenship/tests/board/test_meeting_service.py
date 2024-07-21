from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, time

from authentication.models import User
from citizenship.models.board import Board, Member
from citizenship.service.board import MeetingService


class MeetingServiceTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.board = Board.objects.create(name='Board1', description='Test board')
        self.member1 = Member.objects.create(user=self.user1, board=self.board)
        self.member2 = Member.objects.create(user=self.user2, board=self.board)

    def test_create_meeting(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        self.assertIsNotNone(meeting.id)
        self.assertEqual(meeting.title, 'Test Meeting')
        self.assertEqual(meeting.board, self.board)
        self.assertEqual(meeting.status, 'Scheduled')

    def test_add_session(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        session = MeetingService.add_session(
            meeting_id=meeting.id,
            title='Morning Session',
            date=date(2023, 7, 20),
            start_time=time(9, 0),
            end_time=time(12, 0)
        )
        self.assertIsNotNone(session.id)
        self.assertEqual(session.title, 'Morning Session')
        self.assertEqual(session.meeting, meeting)
        self.assertEqual(session.date, date(2023, 7, 20))
        self.assertEqual(session.start_time, time(9, 0))
        self.assertEqual(session.end_time, time(12, 0))

    def test_add_attendee(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        session = MeetingService.add_session(
            meeting_id=meeting.id,
            title='Morning Session',
            date=date(2023, 7, 20),
            start_time=time(9, 0),
            end_time=time(12, 0)
        )
        attendee = MeetingService.add_attendee(session.id, self.member1.id, confirmed=True)
        self.assertIsNotNone(attendee.id)
        self.assertEqual(attendee.session, session)
        self.assertEqual(attendee.member, self.member1)
        self.assertTrue(attendee.confirmed)

    def test_remove_attendee(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        session = MeetingService.add_session(
            meeting_id=meeting.id,
            title='Morning Session',
            date=date(2023, 7, 20),
            start_time=time(9, 0),
            end_time=time(12, 0)
        )
        attendee = MeetingService.add_attendee(session.id, self.member1.id, confirmed=True)
        self.assertTrue(MeetingService.remove_attendee(session.id, self.member1.id))
        with self.assertRaises(ValidationError):
            MeetingService.remove_attendee(session.id, self.member1.id)

    def test_change_meeting_status(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        updated_meeting = MeetingService.change_meeting_status(meeting.id, 'In Progress')
        self.assertEqual(updated_meeting.status, 'In Progress')

    def test_confirm_attendance(self):
        meeting = MeetingService.create_meeting(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss project updates',
            status='Scheduled'
        )
        session = MeetingService.add_session(
            meeting_id=meeting.id,
            title='Morning Session',
            date=date(2023, 7, 20),
            start_time=time(9, 0),
            end_time=time(12, 0)
        )
        attendee = MeetingService.add_attendee(session.id, self.member1.id, confirmed=False)
        confirmed_attendee = MeetingService.confirm_attendance(session.id, self.member1.id)
        self.assertTrue(confirmed_attendee.confirmed)
