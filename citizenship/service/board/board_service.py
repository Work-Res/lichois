import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import Board, Meeting

logger = logging.getLogger(__name__)


class BoardService:
    @staticmethod
    @transaction.atomic
    def create_board(name, description):
        try:
            board = Board.objects.create(
                name=name,
                description=description
            )
            logger.info(f'Board created: {board}')
            return board
        except Exception as e:
            logger.error(f'Error creating board: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def update_board(board_id, name=None, description=None):
        try:
            board = Board.objects.get(id=board_id)
            if name:
                board.name = name
            if description:
                board.description = description
            board.save()
            logger.info(f'Board updated: {board}')
            return board
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")
        except Exception as e:
            logger.error(f'Error updating board: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def add_board_meeting(board_id, title, location, agenda, status='Scheduled'):
        try:
            board = Board.objects.get(id=board_id)
            if not board.has_quorum():
                raise ValidationError("Board does not meet quorum requirement.")

            meeting = Meeting.objects.create(
                board=board,
                title=title,
                location=location,
                agenda=agenda,
                status=status
            )
            logger.info(f'Meeting created for board {board_id}: {meeting}')
            return meeting
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")
        except Exception as e:
            logger.error(f'Error adding meeting to board: {e}')
            raise
