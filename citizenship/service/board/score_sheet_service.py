import logging
import json

from django.db.models import Count, Avg, Sum, Q
from django.core.serializers.json import DjangoJSONEncoder

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

        json_data = ScoreSheetService.convert_to_json(interview)

        scoresheet = ScoreSheet.objects.create(
            interview=interview,
            total_score=total_score,
            average_score=average_score,
            passed=is_passed,
            aggregated=json_data
        )
        logger.info(
            f"ScoreSheet created for interview {interview.id} with ID {scoresheet.id}"
        )
        return scoresheet

    @staticmethod
    def convert_to_json(interview):
        """
        Converts aggregated interview responses into a JSON format.

        :param interview: The interview instance to aggregate responses for.
        :return: JSON string of aggregated interview data.
        """
        try:
            # Query and aggregate interview responses
            aggregated_data = InterviewResponse.objects.filter(interview=interview).values(
                'text', 'sequence', 'marks_range').annotate(
                total_responses=Count('id'),
                average_score=Avg('score'),
                total_marked=Count('is_marked', filter=Q(is_marked=True)),
                total_unmarked=Count('is_marked', filter=Q(is_marked=False)),
                sum_scores=Sum('score')
            ).order_by('sequence')

            # Convert the queryset into a list
            aggregated_list = list(aggregated_data)

            # If no data, return an empty JSON array
            if not aggregated_list:
                return json.dumps([], cls=DjangoJSONEncoder)

            # Return the aggregated data as a JSON string
            return json.dumps(aggregated_list, cls=DjangoJSONEncoder)

        except InterviewResponse.DoesNotExist:
            # Handle case where interview does not exist
            return json.dumps({"error": "Interview not found"}, cls=DjangoJSONEncoder)

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
