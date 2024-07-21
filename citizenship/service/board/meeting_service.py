import logging

from django.db import transaction
from django.core.exceptions import ValidationError

from citizenship.models.board import Meeting, BoardMember, Attendee, Board
from citizenship.models.board.meeting_session import MeetingSession

logger = logging.getLogger(__name__)


class MeetingService:

    """Responsible for managing creation of meeting, adding meeting attendees and removing e.t.c.
    """
    @staticmethod
    @transaction.atomic
    def create_meeting(title: str, board: Board, date, time, location, agenda: str):
        try:
            meeting = Meeting.objects.create(
                title=title,
                board=board,
                date=date,
                time=time,
                location=location,
                agenda=agenda
            )
            logger.info(f'Meeting created: {meeting}')
            return meeting
        except Exception as e:
            logger.error(f'Error creating meeting: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def add_attendee(session_id, member_id, confirmed=False):
        try:
            session = MeetingSession.objects.get(id=session_id)
            member = BoardMember.objects.get(id=member_id)
            attendee, created = Attendee.objects.get_or_create(
                session=session,
                member=member,
                defaults={'confirmed': confirmed}
            )
            if created:
                logger.info(f'Attendee added: {attendee}')
            else:
                logger.info(f'Attendee already exists: {attendee}')
            return attendee
        except MeetingSession.DoesNotExist:
            logger.error(f'Session does not exist: {session_id}')
            raise ValidationError("Session does not exist.")
        except BoardMember.DoesNotExist:
            logger.error(f'Member does not exist: {member_id}')
            raise ValidationError("Member does not exist.")
        except Exception as e:
            logger.error(f'Error adding attendee: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def remove_attendee(session_id, member_id):
        try:
            attendee = Attendee.objects.get(session_id=session_id, member_id=member_id)
            attendee.delete()
            logger.info(f'Attendee removed: {attendee}')
            return True
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist for session {session_id} and member {member_id}')
            raise ValidationError("Attendee does not exist.")
        except Exception as e:
            logger.error(f'Error removing attendee: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def change_meeting_status(meeting_id, new_status):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            old_status = meeting.status
            meeting.status = new_status
            meeting.save()
            logger.info(f'Meeting status changed from {old_status} to {new_status} for meeting {meeting_id}')
            return meeting
        except Meeting.DoesNotExist:
            logger.error(f'Meeting does not exist: {meeting_id}')
            raise ValidationError("Meeting does not exist.")
        except Exception as e:
            logger.error(f'Error changing meeting status: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def confirm_attendance(meeting_id, member_id, confirmed=False):
        try:
            attendee = Attendee.objects.get(meeting_id=meeting_id, member_id=member_id)
            attendee.confirmed = confirmed
            attendee.save()
            logger.info(f'Attendee {attendee} confirmed attendance for meeting {meeting_id}')
            return attendee
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist for meeting {meeting_id} and member {member_id}')
            raise ValidationError("Attendee does not exist.")
        except Exception as e:
            logger.error(f'Error confirming attendance: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def add_session(meeting_id, title, date, start_time, end_time):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            session = MeetingSession.objects.create(
                meeting=meeting,
                title=title,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            logger.info(f'Session created: {session}')
            return session
        except Meeting.DoesNotExist:
            logger.error(f'Meeting does not exist: {meeting_id}')
            raise ValidationError("Meeting does not exist.")
        except Exception as e:
            logger.error(f'Error creating session: {e}')
            raise

    @staticmethod
    def check_session_conflicts(meeting, date, start_time, end_time):
        sessions = MeetingSession.objects.filter(meeting=meeting, date=date)
        for session in sessions:
            if (start_time < session.end_time and end_time > session.start_time):
                return True
        return False

    @staticmethod
    @transaction.atomic
    def create_session(meeting_id, title, date, start_time, end_time):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            if MeetingService.check_session_conflicts(meeting, date, start_time, end_time):
                raise ValidationError("Meeting Session times conflict with an existing session.")
            session = MeetingSession.objects.create(
                meeting=meeting,
                title=title,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            logger.info(f'Session created: {session}')
            return session
        except Meeting.DoesNotExist:
            logger.error(f'Meeting does not exist: {meeting_id}')
            raise ValidationError("Meeting does not exist.")
        except Exception as e:
            logger.error(f'Error creating session: {e}')
            raise ValidationError("Error creating session.")
