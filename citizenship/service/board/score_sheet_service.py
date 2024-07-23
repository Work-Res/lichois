import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import Interview, ScoreSheet, InterviewQuestion, InterviewDecision

logger = logging.getLogger(__name__)


class ScoreSheetService:
    @staticmethod
    @transaction.atomic
    def create_score_sheet(interview_id):
        try:
            interview = Interview.objects.get(id=interview_id)
            interview_questions = InterviewQuestion.objects.filter(interview=interview)
            total_score = sum(iq.score for iq in interview_questions)
            passed = all(d.passed for d in interview.decisions.all())
            summary = ScoreSheetService.generate_summary(interview)
            score_sheet = ScoreSheet.objects.create(
                interview=interview,
                total_score=total_score,
                passed=passed,
                summary=summary
            )
            logger.info(f'ScoreSheet created: {score_sheet}')
            return score_sheet
        except Interview.DoesNotExist:
            logger.error(f'Interview does not exist: {interview_id}')
            raise ValidationError("Interview does not exist.")
        except Exception as e:
            logger.error(f'Error creating score sheet: {e}')
            raise ValidationError("Error creating score sheet.")

    @staticmethod
    def generate_summary(interview):
        summary_lines = []
        for question in InterviewQuestion.objects.filter(interview=interview):
            summary_lines.append(
                f"Question: {question.question.text}, Score: {question.score}, Member: {question.member.user.username}, Comments: {question.comments}")
        for decision in InterviewDecision.objects.filter(interview=interview):
            summary_lines.append(
                f"Member: {decision.member.user.username}, Passed: {decision.passed}, Reason: {decision.reason}")
        return "\n".join(summary_lines)
