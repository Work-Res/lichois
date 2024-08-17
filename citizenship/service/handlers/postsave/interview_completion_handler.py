import logging
import tempfile

from django.db import models
from django.db import transaction

from citizenship.exception import InterviewCompletionError
from citizenship.exception.interview_score_sheet_error import WordDocumentCreationError, PDFConversionError
from citizenship.models import Interview, InterviewResponse, ScoreSheet, BoardMember
from citizenship.service.word import ScoresheetDocumentGeneratorService, DataGenerator
from citizenship.service.word.data_generator import DataGeneratorException

logger = logging.getLogger(__name__)


class InterviewCompletionHandler:
    def __init__(self, interview: Interview):
        self.interview = interview

    def check_and_create_scoresheet(self):
        try:
            with transaction.atomic():
                # Get all board members for the meeting session's meeting
                members_participated = self.interview.completed_by.all()

                # Check if all board members have submitted their responses
                for member in members_participated:
                    responses = InterviewResponse.objects.filter(
                        interview=self.interview,
                        member=member
                    )
                    print(responses)

                submitted_members = responses.values_list('member', flat=True)
                if set(submitted_members) == set(members_participated.values_list('id', flat=True)):
                    total_score = responses.aggregate(total=models.Sum('score'))['total']
                    average_score = responses.aggregate(avg=models.Avg('score'))['avg']

                    scoresheet = ScoreSheet.objects.create(
                        interview=self.interview,
                        total_score=total_score,
                        average_score=average_score
                    )
                    self.interview.status = 'completed'
                    self.interview.save()
                    logger.info(f"ScoreSheet created for interview {self.interview.id}. Interview marked as complete.")
                    return scoresheet
                else:
                    self.interview.status = 'in_progress'
                    self.interview.save()
                    logger.info(f"Not all board members have submitted responses for interview {self.interview.id}. "
                                f"Status set to in_progress.")
        except Exception as e:
            logger.exception(f"Unexpected error creating scoresheet: {e}")
            raise InterviewCompletionError(e)

    @staticmethod
    def handle_scoresheet_completed(self, scoresheet):
        try:
            logger.info(f"Handling scoresheet completion for scoresheet {scoresheet.id}")

            # Generate data for the PDF using DataGenerator
            data_generator = DataGenerator(scoresheet)
            data = data_generator.generate_data()

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Paths to save the documents
            word_path = f'{temp_dir}/scoresheet_{scoresheet.id}.docx'
            pdf_path = f'{temp_dir}/scoresheet_{scoresheet.id}.pdf'

            # Create the service instance
            service = ScoresheetDocumentGeneratorService(data, word_path, pdf_path)

            # Create and convert the document
            service.create_and_convert()

            # Update the ScoreSheet instance
            scoresheet.document = pdf_path
            scoresheet.save()

            logger.info(f"PDF document created for scoresheet {scoresheet.id} at {pdf_path}")
        except WordDocumentCreationError as e:
            logger.error(f"Word document creation error for scoresheet {scoresheet.id}: {e}")
        except PDFConversionError as e:
            logger.error(f"PDF conversion error for scoresheet {scoresheet.id}: {e}")
        except DataGeneratorException as e:
            logger.error(f"Data generation error for scoresheet {scoresheet.id}: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error creating PDF for scoresheet {scoresheet.id}: {e}")
