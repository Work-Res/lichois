import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import Question

logger = logging.getLogger(__name__)


class QuestionService:
    @staticmethod
    @transaction.atomic
    def create_question(text):
        try:
            question = Question.objects.create(text=text)
            logger.info(f'Question created: {question}')
            return question
        except Exception as e:
            logger.error(f'Error creating question: {e}')
            raise ValidationError("Error creating question.")

    @staticmethod
    def get_question(question_id):
        try:
            question = Question.objects.get(id=question_id)
            logger.info(f'Question retrieved: {question}')
            return question
        except Question.DoesNotExist:
            logger.error(f'Question does not exist: {question_id}')
            raise ValidationError("Question does not exist.")

    @staticmethod
    @transaction.atomic
    def update_question(question_id, text):
        try:
            question = Question.objects.get(id=question_id)
            question.text = text
            question.save()
            logger.info(f'Question updated: {question}')
            return question
        except Question.DoesNotExist:
            logger.error(f'Question does not exist: {question_id}')
            raise ValidationError("Question does not exist.")
        except Exception as e:
            logger.error(f'Error updating question: {e}')
            raise ValidationError("Error updating question.")

    @staticmethod
    @transaction.atomic
    def delete_question(question_id):
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            logger.info(f'Question deleted: {question}')
            return True
        except Question.DoesNotExist:
            logger.error(f'Question does not exist: {question_id}')
            raise ValidationError("Question does not exist.")
        except Exception as e:
            logger.error(f'Error deleting question: {e}')
            raise ValidationError("Error deleting question.")
