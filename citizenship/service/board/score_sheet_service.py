import logging
from math import log
from re import S

from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from app_checklist.models import SystemParameterMarkingKey
from citizenship.models import Interview, ScoreSheet, InterviewResponse

logger = logging.getLogger(__name__)


class ScoreSheetService:

    @staticmethod
    @transaction.atomic
    def create_scoresheet(interview: Interview):
        logger.info(f"Creating scoresheet for interview {interview.id}")
        total_score = InterviewResponse.objects.filter(interview=interview).aggregate(
            total=models.Sum("score")
        )["total"]
        logger.info(f"Total score for interview {interview.id}: {total_score}")
        average_score = total_score / interview.completed_by.all().count()

        logger.info(f"Average score for interview {interview.id}: {average_score}")
        system_parameter_marking_key = SystemParameterMarkingKey.objects.get(
            code=f"{interview.variation_type}_marking_key"
        )

        is_passed = int(average_score) >= int(
            system_parameter_marking_key.pass_mark_in_percent
        )
        logger.info(f"Interview {interview.id} passed: {is_passed}")

        scoresheet = ScoreSheet.objects.create(
            interview=interview,
            total_score=total_score,
            average_score=average_score,
            passed=is_passed,
        )
        logger.info(
            f"ScoreSheet created for interview {interview.id} with ID {scoresheet.id}"
        )
        return scoresheet

    @staticmethod
    def get_score_sheet(score_sheet_id):
        try:
            return ScoreSheet.objects.get(id=score_sheet_id)
        except ScoreSheet.DoesNotExist:
            raise ValidationError("Score sheet does not exist.")

    @staticmethod
    def list_score_sheets():
        return ScoreSheet.objects.all()

    @staticmethod
    def list_score_sheet_details(score_sheet_id):
        try:
            score_sheet = ScoreSheet.objects.get(id=score_sheet_id)
            return score_sheet.aggregated_responses
        except ScoreSheet.DoesNotExist:
            raise ValidationError("Score sheet does not exist.")
