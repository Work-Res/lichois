import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from citizenship.models import ScoreSheet
from citizenship.models.board.board_recommandation import BoardRecommendation

logger = logging.getLogger(__name__)


class BoardRecommendationService:
    @staticmethod
    @transaction.atomic
    def create_board_recommendation(document_number, recommendation, reason=''):
        try:
            score_sheet = ScoreSheet.objects.get(
                interview__application__application_document__document_number=document_number)
            if recommendation == 'Denied' and not reason:
                raise ValidationError("Reason is required when the recommendation is denied.")
            board_recommendation = BoardRecommendation.objects.create(
                score_sheet=score_sheet,
                recommendation=recommendation,
                reason=reason
            )
            logger.info(f'BoardRecommendation created: {board_recommendation}')
            return board_recommendation
        except ScoreSheet.DoesNotExist:
            logger.error(f'ScoreSheet does not exist: {document_number}')
            raise ValidationError("ScoreSheet does not exist.")
        except Exception as e:
            logger.error(f'Error creating board recommendation: {e}')
            raise ValidationError(f"Error creating board recommendation. {e}")
