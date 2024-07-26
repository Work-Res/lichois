from django.core.exceptions import ValidationError
from django.db import transaction
from citizenship.models import Interview, ScoreSheet


class ScoreSheetService:

    @staticmethod
    @transaction.atomic
    def create_score_sheet(interview_id, total_score, aggregated_responses, passed, summary):
        try:
            interview = Interview.objects.get(id=interview_id)

            score_sheet = ScoreSheet.objects.create(
                interview=interview,
                total_score=total_score,
                aggregated_responses=aggregated_responses,
                passed=passed,
                summary=summary
            )

            return score_sheet
        except Interview.DoesNotExist:
            raise ValidationError("Interview does not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating score sheet: {str(e)}")

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
