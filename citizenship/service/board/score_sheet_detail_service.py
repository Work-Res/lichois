from django.core.exceptions import ValidationError
from django.db import transaction
from citizenship.models import ScoreSheetDetail, ScoreSheet, InterviewQuestion


class ScoreSheetDetailService:

    @staticmethod
    @transaction.atomic
    def create_score_sheet_detail(score_sheet_id, question_id, aggregated_score, aggregated_responses):
        try:
            score_sheet = ScoreSheet.objects.get(id=score_sheet_id)
            question = InterviewQuestion.objects.get(id=question_id)

            score_sheet_detail = ScoreSheetDetail.objects.create(
                score_sheet=score_sheet,
                question=question,
                aggregated_score=aggregated_score,
                aggregated_responses=aggregated_responses
            )

            return score_sheet_detail
        except ScoreSheet.DoesNotExist:
            raise ValidationError("ScoreSheet does not exist.")
        except InterviewQuestion.DoesNotExist:
            raise ValidationError("InterviewQuestion does not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating ScoreSheetDetail: {str(e)}")

    @staticmethod
    def get_score_sheet_detail(score_sheet_detail_id):
        try:
            return ScoreSheetDetail.objects.get(id=score_sheet_detail_id)
        except ScoreSheetDetail.DoesNotExist:
            raise ValidationError("ScoreSheetDetail does not exist.")

    @staticmethod
    def list_score_sheet_details(score_sheet_id=None):
        try:
            if score_sheet_id:
                return ScoreSheetDetail.objects.filter(score_sheet_id=score_sheet_id)
            return ScoreSheetDetail.objects.all()
        except Exception as e:
            raise ValidationError(f"Error listing ScoreSheetDetails: {str(e)}")

    @staticmethod
    @transaction.atomic
    def update_score_sheet_detail(score_sheet_detail_id, aggregated_score=None, aggregated_responses=None):
        try:
            score_sheet_detail = ScoreSheetDetail.objects.get(id=score_sheet_detail_id)
            if aggregated_score is not None:
                score_sheet_detail.aggregated_score = aggregated_score
            if aggregated_responses is not None:
                score_sheet_detail.aggregated_responses = aggregated_responses
            score_sheet_detail.save()
            return score_sheet_detail
        except ScoreSheetDetail.DoesNotExist:
            raise ValidationError("ScoreSheetDetail does not exist.")
        except Exception as e:
            raise ValidationError(f"Error updating ScoreSheetDetail: {str(e)}")

    @staticmethod
    @transaction.atomic
    def delete_score_sheet_detail(score_sheet_detail_id):
        try:
            score_sheet_detail = ScoreSheetDetail.objects.get(id=score_sheet_detail_id)
            score_sheet_detail.delete()
            return True
        except ScoreSheetDetail.DoesNotExist:
            raise ValidationError("ScoreSheetDetail does not exist.")
        except Exception as e:
            raise ValidationError(f"Error deleting ScoreSheetDetail: {str(e)}")