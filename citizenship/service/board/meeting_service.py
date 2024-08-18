import logging

from django.db import transaction

from django.core.exceptions import ValidationError

from citizenship.models import Meeting, BoardMember, Attendee, Board
from citizenship.models.board.meeting_session import MeetingSession

logger = logging.getLogger(__name__)


class MeetingService:

    """Responsible for managing creation of meeting, adding meeting attendees and removing e.t.c.
    """
    @staticmethod
    @transaction.atomic
    def create_meeting(title, board_id, location, agenda, start_date, end_date, time):
        try:
            board = Board.objects.get(id=board_id)
            if MeetingService.check_meeting_conflicts(board, start_date, end_date):
                raise ValidationError("A meeting for the same board already exists in the specified period.")
            meeting = Meeting.objects.create(
                title=title,
                board=board,
                location=location,
                agenda=agenda,
                start_date=start_date,
                end_date=end_date,
                time=time
            )
            logger.info(f'Meeting created: {meeting}')
            MeetingService.create_attendances_for_meeting(meeting)
            return meeting
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")
        except Exception as e:
            logger.error(f'Error creating meeting: {e}')
            raise ValidationError("Error creating meeting.")

    @staticmethod
    @transaction.atomic
    def add_attendee(meeting, member_id, confirmed=False):
        try:
            member = BoardMember.objects.get(id=member_id)
            attendee, created = Attendee.objects.get_or_create(
                member=member,
                meeting=meeting,
                defaults={'confirmed': confirmed}
            )
            if created:
                logger.info(f'Attendee added: {attendee}')
            else:
                logger.info(f'Attendee already exists: {attendee}')
            return attendee
        except BoardMember.DoesNotExist:
            logger.error(f'Member does not exist: {member_id}')
            raise ValidationError("Member does not exist.")
        except Exception as e:
            logger.error(f'Error adding attendee: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def remove_attendee(meeting_id, member_id):
        try:
            attendee = Attendee.objects.get(meeting_id=meeting_id, member_id=member_id)
            attendee.delete()
            logger.info(f'Attendee removed: {attendee}')
            return True
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist for session {meeting_id} and member {member_id}')
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
    def confirm_attendance(meeting_id, member_id, confirmed=False, proposed_date=None):
        try:
            attendee = Attendee.objects.get(meeting_id=meeting_id, member_id=member_id)
            if proposed_date:
                attendee.proposed_date = proposed_date
                attendee.confirmed = False
                logger.info(f'Attendee {attendee} proposed a new date for meeting {meeting_id}: {proposed_date}')
            else:
                attendee.confirmed = confirmed
                attendee.proposed_date = None
                logger.info(f'Attendee {attendee} confirmed attendance for meeting {meeting_id}')
            attendee.save()
            return attendee
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist for meeting {meeting_id} and member {member_id}')
            raise ValidationError("Attendee does not exist.")
        except Exception as e:
            logger.error(f'Error confirming attendance: {e}')
            raise

    @staticmethod
    def create_attendances_for_meeting(meeting):
        try:
            members = BoardMember.objects.filter(board=meeting.board)
            for member in members:
                Attendee.objects.create(meeting=meeting, member=member)
                logger.info(f'Attendee created: {member.user.username} for meeting {meeting.title}')
        except Exception as e:
            logger.error(f'Error creating attendees for meeting: {e}')
            raise ValidationError("Error creating attendees for meeting.")

    @staticmethod
    def check_meeting_conflicts(board, start_date, end_date):
        meetings = Meeting.objects.filter(board=board)
        for meeting in meetings:
            if start_date <= meeting.end_date and end_date >= meeting.start_date:
                return True
        return False

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
