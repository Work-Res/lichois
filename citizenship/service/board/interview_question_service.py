import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import InterviewQuestion, Interview, Question, Member
from citizenship.service.board.interview_completion_service import InterviewCompletionService

logger = logging.getLogger(__name__)


class InterviewQuestionService:
    @staticmethod
    @transaction.atomic
    def create_interview_question(interview_id, question_text, score, member_id, comments='', is_marked=False):
        try:
            interview = Interview.objects.get(id=interview_id)
            question, created = Question.objects.get_or_create(text=question_text)
            member = Member.objects.get(id=member_id)
            interview_question = InterviewQuestion.objects.create(
                interview=interview,
                question=question,
                member=member,
                score=score,
                comments=comments,
                is_marked=is_marked
            )
            if is_marked:
                InterviewCompletionService.mark_interview_as_completed(interview_id, member_id)
            logger.info(f'InterviewQuestion created: {interview_question}')
            return interview_question
        except Interview.DoesNotExist:
            logger.error(f'Interview does not exist: {interview_id}')
            raise ValidationError("Interview does not exist.")
        except Member.DoesNotExist:
            logger.error(f'Member does not exist: {member_id}')
            raise ValidationError("Member does not exist.")
        except Exception as e:
            logger.error(f'Error creating interview question: {e}')
            raise ValidationError("Error creating interview question.")

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
    def update_interview_question(interview_question_id, question_text=None, score=None, comments=None, is_marked=None):
        try:
            interview_question = InterviewQuestion.objects.get(id=interview_question_id)
            if question_text is not None:
                question, created = Question.objects.get_or_create(text=question_text)
                interview_question.question = question
            if score is not None:
                interview_question.score = score
            if comments is not None:
                interview_question.comments = comments
            if is_marked is not None:
                interview_question.is_marked = is_marked
            if is_marked:
                InterviewCompletionService.mark_interview_as_completed(interview_question.interview.id,
                                                                       interview_question.member.id)
                interview_question.save()

                logger.info(f'InterviewQuestion updated: {interview_question}')
                return interview_question
        except InterviewQuestion.DoesNotExist:
            logger.error(f'InterviewQuestion does not exist: {interview_question_id}')
            raise ValidationError('InterviewQuestion does not exist.')
        except Exception as e:
            logger.error(f'Error updating interview question: {e}')
            raise ValidationError('Error updating interview question.')
