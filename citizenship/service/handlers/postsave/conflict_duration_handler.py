import logging

from pathlib import Path
from django.core.exceptions import ObjectDoesNotExist

from citizenship.exception.conflict_duration_error import ConflictDurationError
from citizenship.models import BatchApplication, ConflictOfInterest, BoardMember, Interview, InterviewResponse
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from citizenship.service.board import InterviewResponseImportService

logger = logging.getLogger(__name__)


class ConflictDurationHandler:
    """
    Handler class for processing conflict of interest durations.

    Attributes:
        conflict_duration (ConflictOfInterestDuration): The conflict duration instance being processed.
    """

    def __init__(self, conflict_duration: ConflictOfInterestDuration, csv_path: str = None):

        """
        Initializes the handler with the conflict duration instance.

        Args:
            conflict_duration (ConflictOfInterestDuration): The conflict duration instance being processed.
        """
        self.conflict_duration = conflict_duration
        self.csv_path = csv_path

    def process(self):
        """
        Processes the conflict duration.
        """
        if self.conflict_duration.status == 'completed':
            self._handle_completed_duration()

    def interview(self, application):
        interview = application.applications
        logger.info(f"Preparing to create interview responses for {interview} interview.")
        self.csv_path = Path(
            "citizenship") / "service" / "board" / "configurations" / "interviews" / f"{interview.variation_type}_questions.csv"
        logger.info(f"Scoresheet variation configuration path: {self.csv_path}")
        return interview

    def _handle_completed_duration(self):
        """
        Handles the completion of the conflict duration.
        """
        meeting_session = self.conflict_duration.meeting_session
        batch_applications = BatchApplication.objects.filter(meeting_session=meeting_session)

        for batch_application in batch_applications:
            application = batch_application.application
            board_members = self._get_board_members_for_interview(application, meeting_session.meeting.board)
            self.interview(application)

            service = InterviewResponseImportService(self.csv_path)
            service.read_csv()

            self._create_interview_responses_for_members(meeting_session, application, board_members, service.data)

        logger.info(f"Duration for session {meeting_session} is now completed.")

    def _get_board_members_for_interview(self, application, board):
        """
        Retrieves board members who have explicitly declared no conflict of interest for the given application.
        Excludes those who have either declared a conflict or have not made any declaration.
        """
        members_with_no_conflict = ConflictOfInterest.objects.filter(
            application=application, has_conflict=False
        ).values_list('attendee__member_id', flat=True)

        return BoardMember.objects.filter(
            board=board,
            id__in=members_with_no_conflict
        ).distinct()

    def _create_interview_responses_for_members(self, meeting_session, application, members, data):
        """
        Creates interview responses for the provided members.
        """
        for member in members:
            self._create_interview_responses(meeting_session, application, member, data)
            logger.info(f"Created interview responses for member {member.id} for application {application.id}")

    def _create_interview_responses(self, meeting_session, application, member, data):
        """
        Creates interview responses for the specified meeting session, application, and member.

        Args:
            meeting_session (MeetingSession): The meeting session instance.
            application (Application): The application instance.
            member (BoardMember): The board member instance.
            data (list): The list of interview response data.
        """
        for row in data:
            try:
                interview = Interview.objects.get(meeting_session=meeting_session, application=application)
                interview_response = InterviewResponse.objects.create(
                    interview=interview,
                    member=member,
                    text=row['text'],
                    category=row['category'],
                    marks_range=row['marks_range'] if row['marks_range'] else None,
                    sequence=row['order']
                )
                logger.info(f"Created InterviewResponse: {interview_response}")
            except ObjectDoesNotExist as e:
                logger.error(f"Object does not exist: {e}")
            except ValueError as e:
                logger.error(f"ValueError: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error processing row: {e}")
                raise ConflictDurationError(e)
