import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from app_checklist.models import Region
from citizenship.models import Board, Role


logger = logging.getLogger(__name__)


class BoardService:
    @staticmethod
    @transaction.atomic
    def create_board(name, region_id, description, quorum_role_ids):
        try:
            region = Region.objects.get(pk=region_id)
            board = Board.objects.create(
                name=name,
                region=region,
                description=description
            )
            roles = Role.objects.filter(id__in=quorum_role_ids)
            board.quorum_roles.set(roles)
            board.save()
            logger.info(f'Board created: {board}')
            return board
        except Region.DoesNotExist:
            logger.error(f'Region does not exist: {region_id}')
            raise ValidationError("Region does not exist.")
        except Exception as e:
            logger.error(f'Error creating board: {e}')
            raise ValidationError("Error creating board.")

    @staticmethod
    def get_board(board_id):
        try:
            board = Board.objects.get(id=board_id)
            logger.info(f'Board retrieved: {board}')
            return board
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")

    @staticmethod
    @transaction.atomic
    def update_board(board_id, name=None, region_id=None, description=None, quorum_role_ids=None):
        try:
            board = Board.objects.get(id=board_id)
            if name:
                board.name = name
            if region_id:
                region = Region.objects.get(id=region_id)
                board.region = region
            if description:
                board.description = description
            if quorum_role_ids:
                roles = Role.objects.filter(id__in=quorum_role_ids)
                board.quorum_roles.set(roles)
            board.save()
            logger.info(f'Board updated: {board}')
            return board
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")
        except Region.DoesNotExist:
            logger.error(f'Region does not exist: {region_id}')
            raise ValidationError("Region does not exist.")
        except Exception as e:
            logger.error(f'Error updating board: {e}')
            raise ValidationError("Error updating board.")

    @staticmethod
    @transaction.atomic
    def delete_board(board_id):
        try:
            board = Board.objects.get(id=board_id)
            board.delete()
            logger.info(f'Board deleted: {board}')
            return True
        except Board.DoesNotExist:
            logger.error(f'Board does not exist: {board_id}')
            raise ValidationError("Board does not exist.")
        except Exception as e:
            logger.error(f'Error deleting board: {e}')
            raise ValidationError("Error deleting board.")