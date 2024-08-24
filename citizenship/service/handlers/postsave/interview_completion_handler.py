import logging
import tempfile

from django.db import models
from django.db import transaction

from citizenship.exception import InterviewCompletionError
from citizenship.exception.interview_score_sheet_error import (
    WordDocumentCreationError,
    PDFConversionError,
)
from citizenship.models import Interview, InterviewResponse, ScoreSheet, BoardMember
from ...board.score_sheet_service import ScoreSheetService
from citizenship.service.word import (
    ScoresheetDocumentGeneratorService,
    DataGenerator,
    DocumentGenerationService,
)
from citizenship.service.word.data_generator import DataGeneratorException

logger = logging.getLogger(__name__)


class InterviewCompletionHandler:
    def __init__(self, interview: Interview, score_sheet_service: ScoreSheetService):
        self.interview = interview
        self.score_sheet_service = score_sheet_service

    def check_and_complete_interview(self):
        logger.info(
            f"Starting check_and_complete_interview for interview {self.interview.id}"
        )
        try:
            if self._all_responses_submitted():
                scoresheet = self.score_sheet_service.create_scoresheet(
                    interview=self.interview
                )
                return scoresheet
            else:
                self.interview.status = "in_progress"
                self.interview.save()
                logger.info(
                    f"Not all board members have submitted responses for interview {self.interview.id}. Status set to in_progress."
                )
                raise InterviewCompletionError(
                    "Not all board members have submitted responses."
                )
        except Exception as e:
            logger.error(
                f"Unexpected error completing interview {self.interview.id}: {e}"
            )
            raise InterviewCompletionError(e)
        finally:
            logger.info(
                f"Finished check_and_complete_interview for interview {self.interview.id}"
            )

    def _all_responses_submitted(self):
        members_participated = self.interview.completed_by.all()
        logger.info(f"Total members who participated: {members_participated.count()}")

        for member in members_participated:
            # Check for any responses with is_marked=False
            unmarked_responses_exist = InterviewResponse.objects.filter(
                interview=self.interview, member=member, is_marked=False
            ).exists()

            if unmarked_responses_exist:
                logger.info(f"Unmarked responses found for member {member.id}.")
                return False

            # Check if the member has at least one marked response
            marked_responses_exist = InterviewResponse.objects.filter(
                interview=self.interview, member=member, is_marked=True
            ).exists()

            if not marked_responses_exist:
                logger.info(f"No marked responses found for member {member.id}.")
                return False

            logger.debug(f"All responses for member {member.id} are marked.")

        logger.info("All members have submitted marked responses.")
        return True


class InterviewCompletionHandlerFactory:
    @staticmethod
    def create(interview: Interview):
        score_sheet_service = ScoreSheetService()
        document_generation_service = DocumentGenerationService()
        return InterviewCompletionHandler(interview, score_sheet_service)
