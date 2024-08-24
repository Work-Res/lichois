import logging

from django.db import models

from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from app.models import Application
from citizenship.models import Interview, MeetingSession, BoardMember, InterviewResponse, ScoreSheet

logger = logging.getLogger(__name__)


class InterviewService:
    def __init__(self, meeting_session: MeetingSession = None, application: Application = None,
                 scheduled_time: timezone = None):
        self.meeting_session = meeting_session
        self.application = application
        self.scheduled_time = scheduled_time

    @transaction.atomic
    def create_interview(self):
        try:
            if Interview.objects.filter(application=self.application).exists():
                logger.error("An interview for this application already exists.")
                raise ValidationError("An interview for this application already exists.")

            interview = Interview.objects.create(
                meeting_session=self.meeting_session,
                application=self.application,
                scheduled_time=self.scheduled_time,
                conducted=False
            )
            logger.info(f"Interview created for application {self.application.id} at {self.scheduled_time}.")
            return interview
        except ValidationError as e:
            logger.error(f"Error creating interview: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error creating interview: {e}")
            raise

    def check_and_create_scoresheet(self, interview: Interview):
        try:
            # Get all board members for the meeting session
            board_members = BoardMember.objects.filter(board=interview.meeting_session.meeting.board)

            # Check if all board members have submitted their responses
            responses = InterviewResponse.objects.filter(interview=interview)
            submitted_members = responses.values_list('member', flat=True)
            print()
            if set(submitted_members) == set(board_members.values_list('id', flat=True)):
                total_score = responses.aggregate(total=models.Sum('score'))['total']
                average_score = responses.aggregate(avg=models.Avg('score'))['avg']

                scoresheet = ScoreSheet.objects.create(
                    interview=interview,
                    total_score=total_score,
                    average_score=average_score
                )
                interview.status = 'completed'
                interview.save()
                logger.info(f"ScoreSheet created for interview {interview.id}. Interview marked as complete.")
                return scoresheet
            else:
                interview.status = 'in_progress'
                interview.save()
                logger.info(
                    f"Not all board members have submitted responses for interview {interview.id}. Status set to in_progress.")
        except Exception as e:
            logger.exception(f"Unexpected error creating scoresheet: {e}")
            raise ValidationError(e)

    @transaction.atomic
    def update_interview(self, interview: Interview, scheduled_time: timezone = None, conducted: bool = None):
        try:
            if scheduled_time is not None:
                interview.scheduled_time = scheduled_time
            if conducted is not None:
                interview.conducted = conducted
            interview.save()
            logger.info(f"Interview {interview.id} updated.")
            return interview
        except ObjectDoesNotExist:
            logger.error("Interview does not exist.")
            raise ValidationError("Interview does not exist.")
        except Exception as e:
            logger.exception(f"Unexpected error updating interview: {e}")
            raise

    @transaction.atomic
    def update_interview_by_application_id(self, application_id: int, conducted: bool, status: str):
        try:
            interview = Interview.objects.get(application__id=application_id)
            interview.conducted = conducted
            interview.status = status
            interview.save()
            logger.info(f"Interview for application {application_id} updated: conducted={conducted}, status={status}.")
            return interview
        except Interview.DoesNotExist:
            logger.error(f"Interview does not exist for application ID {application_id}.")
            raise ValidationError("Interview does not exist for the given application ID.")
        except Exception as e:
            logger.error(f"Unexpected error updating interview for application ID {application_id}: {e}")
            raise

    @transaction.atomic
    def add_board_member(self, interview: Interview = None, board_member: BoardMember = None):
        try:
            if not interview:
                interview = Interview.objects.get(application=self.application)
            interview.completed_by.add(board_member)
            logger.info(f"Board member {board_member.id} added to interview {interview.id}.")
            return interview
        except Interview.DoesNotExist:
            logger.error(f"Interview record not found for {self.application.application_document.document_number}")
        except Exception as e:
            logger.exception(f"Unexpected error adding board member to interview: {e}")
            raise

    @transaction.atomic
    def remove_board_member(self, interview: Interview, board_member: BoardMember):
        try:
            interview.completed_by.remove(board_member)
            logger.info(f"Board member {board_member.id} removed from interview {interview.id}.")
            return interview
        except Exception as e:
            logger.exception(f"Unexpected error removing board member from interview: {e}")
            raise

    @transaction.atomic
    def delete_interview(self, interview: Interview):
        try:
            interview_id = interview.id
            interview.delete()
            logger.info(f"Interview {interview_id} deleted.")
        except ObjectDoesNotExist:
            logger.error("Interview does not exist.")
            raise ValidationError("Interview does not exist.")
        except Exception as e:
            logger.exception(f"Unexpected error deleting interview: {e}")
            raise


# Usage example
def schedule_interview(meeting_session_id, application_id, scheduled_time):
    try:
        meeting_session = MeetingSession.objects.get(id=meeting_session_id)
        application = Application.objects.get(id=application_id)
        service = InterviewService(meeting_session, application, scheduled_time)
        return service.create_interview()
    except ObjectDoesNotExist as e:
        logger.error(f"Error scheduling interview: {e}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
