import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from authentication.models import User
from gazette.exceptions import BatchNotFoundException, UserNotFoundException
from gazette.models import Batch, LegalAssessment, BatchApplication
from gazette.models.batch_decision import BatchDecision
from gazette.service.notification_service import NotificationService

logger = logging.getLogger(__name__)


class BatchDecisionService:
    @staticmethod
    @transaction.atomic
    def create_batch_decision(batch_id, legal_member_id, decision, comments):
        try:
            batch = Batch.objects.get(id=batch_id)
            applications = BatchApplication.objects.filter(batch=batch)
            legal_member = User.objects.get(id=legal_member_id)

            # Ensure all assessments are completed before making a decision
            incomplete_assessments = []
            for application in applications:
                incomplete_assessments = LegalAssessment.objects.filter(application=application, status='IN_PROGRESS')
                if incomplete_assessments.exists:
                    incomplete_assessments.append(incomplete_assessments.first())

            if len(incomplete_assessments) > 0:
                raise ValueError("All assessments must be completed before making a batch decision.")

            batch_decision = BatchDecision.objects.create(
                batch=batch,
                decision=decision,
                comments=comments
            )

            # Update batch status to 'REVIEWED' if approved, otherwise keep it as is
            if decision == 'APPROVED':
                batch.status = 'APPROVED'
                batch.save()

            logger.info(f"Batch decision created for batch ID {batch_id} by user {legal_member.username}")
            NotificationService.notify_ag_group(batch)
            return batch_decision
        except ObjectDoesNotExist as e:
            if 'Batch' in str(e):
                logger.error(f"Batch with ID {batch_id} does not exist")
                raise BatchNotFoundException()
            elif 'User' in str(e):
                logger.error(f"User with ID {legal_member_id} does not exist")
                raise UserNotFoundException()
        except ValueError as ve:
            logger.error(str(ve))
            raise
