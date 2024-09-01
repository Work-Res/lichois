import datetime
from django.test import tag
from datetime import date
from django.utils import timezone

from app_checklist.models import Region, Holiday
from authentication.models import User
from citizenship.models.board.role import Role
from citizenship.models import Meeting, MeetingSession, Board, BoardMember
from citizenship.service.board import MeetingSessionService

from .base_setup import BaseSetup


@tag('mss')
class MeetingSessionServiceTestCase(BaseSetup):

    def create_holiday(self, internal=1):
        Holiday.objects.create(
            name="",
            description="",
            is_public_holiday=True,
            holiday_date=timezone.now() + timezone.timedelta(days=internal),
            valid_from=timezone.now(),
            valid_to =timezone.now() + timezone.timedelta(days=internal),
            year="2024"
        )

    def setUp(self):
        super(MeetingSessionServiceTestCase, self).setUp()
        self.role = Role.objects.create(name="SE", description="Software engineee")
        self.user = User.objects.create_user(username="test", password='testpass')
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
        self.member = BoardMember.objects.create(
            user=self.user, board=self.board, role=self.role)

        # Create Meeting
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            board=self.board,
            location='Conference Room',
            agenda='Discuss Q3 targets',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=5),
            time=datetime.time(9, 0)
        )

    def test_generate_recurring_sessions(self):

        self.meeting_session = MeetingSession.objects.create(
            meeting=self.meeting,
            title='Morning Session',
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            is_recurring=True
        )

        # Query the database for all sessions related to this meeting
        all_sessions = MeetingSession.objects.filter(meeting=self.meeting)

        # We expect 5 sessions (one for each day from January 1st to January 5th)
        self.assertEqual(all_sessions.count(), 5)
        session1 = MeetingSession.objects.first()
        session2 = MeetingSession.objects.last()
        self.assertNotEqual(session1.date, session2.date)

    def test_generate_recurring_sessions_skipping_holidays(self):
        # service = MeetingSessionService(self.meeting_session)
        # service.generate_recurring_sessions()
        self.create_holiday(internal=5)
        self.create_holiday(internal=4)
        MeetingSession.objects.all().delete()
        # Query the database for all sessions related to this meeting
        self.meeting_session = MeetingSession.objects.create(
            meeting=self.meeting,
            title='Morning Session',
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            is_recurring=True
        )

        all_sessions = MeetingSession.objects.filter(meeting=self.meeting)

        # We expect 5 sessions (one for each day from January 1st to January 5th)
        self.assertEqual(all_sessions.count(), 3)
        session1 = MeetingSession.objects.first()
        session2 = MeetingSession.objects.last()
        self.assertNotEqual(session1.date, session2.date)

    def test_no_recurring_sessions_when_no_end_date(self):
        # Set the meeting's end date to None
        self.meeting.end_date = None
        self.meeting.save()

        service = MeetingSessionService(self.meeting_session)
        service.generate_recurring_sessions()

        # No additional sessions should be created
        all_sessions = MeetingSession.objects.filter(meeting=self.meeting)
        self.assertEqual(all_sessions.count(), 2)  # Only the original session should exist

    def test_no_recurring_sessions_when_start_date_after_end_date(self):
        # Set the session's date after the meeting's end date
        self.meeting_session.date = date(2024, 1, 6)
        self.meeting_session.save()

        service = MeetingSessionService(self.meeting_session)
        sessions = service.generate_recurring_sessions()

        # No additional sessions should be created
        all_sessions = MeetingSession.objects.filter(meeting=self.meeting)
        self.assertEqual(all_sessions.count(), 1)  # Only the original session should exist
