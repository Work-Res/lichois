import logging
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

    def __init__(self, conflict_duration: ConflictOfInterestDuration, csv_path: str):

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

    def _handle_completed_duration(self):
        """
        Handles the completion of the conflict duration.
        """
        meeting_session = self.conflict_duration.meeting_session
        batch_applications = BatchApplication.objects.filter(meeting_session=meeting_session)
        service = InterviewResponseImportService(self.csv_path)
        service.read_csv()

        for batch_application in batch_applications:
            application = batch_application.application
            meeting = meeting_session.meeting
            board_members = BoardMember.objects.filter(board=meeting.board)
            for member in board_members:
                if not ConflictOfInterest.objects.filter(
                        attendee__member=member, application=application, has_conflict=True).exists():
                    self._create_interview_responses(meeting_session, application, member, service.data)

        logger.info(f"Duration for session {self.conflict_duration.meeting_session} is now completed.")

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
                    marks_range=int(row['marks_range']) if row['marks_range'] else None
                )
                logger.info(f"Created InterviewResponse: {interview_response}")
            except ObjectDoesNotExist as e:
                logger.error(f"Object does not exist: {e}")
            except ValueError as e:
                logger.error(f"ValueError: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error processing row: {e}")
                raise ConflictDurationError(e)
