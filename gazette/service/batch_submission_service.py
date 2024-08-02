import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from gazette.exceptions import InvalidBatchStatusException, BatchNotFoundException
from gazette.models import Batch

logger = logging.getLogger(__name__)


class BatchSubmissionService:
    @staticmethod
    @transaction.atomic
    def submit_batch(batch_id):
        try:
            batch = Batch.objects.get(id=batch_id)
            batch.status = 'RECOMMANDED'
            batch.save()
            logger.info(f"Batch with ID {batch_id} recommanded")
            # NotificationService.notify_legal_person(batch)
        except ObjectDoesNotExist as e:
            logger.error(f"Batch with ID {batch_id} does not exist")
            raise BatchNotFoundException()

    @staticmethod
    @transaction.atomic
    def update_batch_status(batch_id, status):
        try:
            batch = Batch.objects.get(id=batch_id)
            batch.status = status
            batch.save()
            logger.info(f"Batch with ID {batch_id} status updated to {status}")
        except ObjectDoesNotExist as e:
            logger.error(f"Batch with ID {batch_id} does not exist")
            raise BatchNotFoundException()
