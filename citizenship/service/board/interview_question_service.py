import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models import InterviewQuestion, Meeting

logger = logging.getLogger(__name__)


class InterviewQuestionService:

    @staticmethod
    @transaction.atomic
    def create_interview_question(meeting_id, text):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            interview_question = InterviewQuestion.objects.create(
                meeting=meeting,
                text=text
            )
            return interview_question
        except Meeting.DoesNotExist:
            raise ValidationError("Meeting does not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating interview question: {str(e)}")

    @staticmethod
    def get_interview_question(interview_question_id):
        try:
            interview_question = InterviewQuestion.objects.get(id=interview_question_id)
            logger.info(f'InterviewQuestion retrieved: {interview_question}')
            return interview_question
        except InterviewQuestion.DoesNotExist:
            logger.error(f'InterviewQuestion does not exist: {interview_question_id}')
            raise ValidationError("InterviewQuestion does not exist.")

    @staticmethod
    @transaction.atomic
    def update_interview_question(question_id, text):
        try:
            interview_question = InterviewQuestion.objects.get(id=question_id)
            interview_question.text = text
            interview_question.save()
            return interview_question
        except InterviewQuestion.DoesNotExist:
            raise ValidationError("Interview question does not exist.")
        except Exception as e:
            raise ValidationError(f"Error updating interview question: {str(e)}")
