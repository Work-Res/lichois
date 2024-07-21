import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from citizenship.models.board import ScoreSheet
from citizenship.models.board.board_recommandation import BoardRecommendation

logger = logging.getLogger(__name__)


class BoardRecommendationService:
    @staticmethod
    @transaction.atomic
    def create_board_recommendation(score_sheet_id, recommendation, reason=''):
        try:
            score_sheet = ScoreSheet.objects.get(id=score_sheet_id)
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
            logger.error(f'ScoreSheet does not exist: {score_sheet_id}')
            raise ValidationError("ScoreSheet does not exist.")
        except Exception as e:
            logger.error(f'Error creating board recommendation: {e}')
            raise ValidationError("Error creating board recommendation.")
