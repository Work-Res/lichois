import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from board.choices import CANCELLED, ENDED
from board.classes.voting_decision_manager import VotingDecisionManager
from board.models import (
    Agenda,
    ApplicationBatch,
    BoardDecision,
    BoardMeeting,
    VotingProcess,
)

from workresidentpermit.classes.service import WorkResidentPermitDecisionService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@receiver(post_save, sender=BoardDecision)
def create_application_decision(sender, instance, created, **kwargs):
    try:
        if created:
            logger.info(f"Creating application decision for document_number: {instance.document_number}")
            work_resident_permit_decision_service = WorkResidentPermitDecisionService(
                document_number=instance.document_number,
                board_decision=instance,
            )
            work_resident_permit_decision_service.create_application_decision()
            work_resident_permit_decision_service.update_application()
            logger.info(f"Successfully created and updated application decision for document_number: {instance.document_number}")
        else:
            logger.info(
                f"BoardDecision: No action required for document_number: {instance.document_number}")
    except SystemError as e:
        logger.error(
            f"SystemError: An error occurred while creating new application decision for document_number: {instance.document_number}",
            exc_info=True
        )
    except Exception as ex:
        logger.error(
            f"An unexpected error occurred while trying to create application decision for document_number: {instance.document_number}",
            exc_info=True  # Logs the full stack trace for any other exception
        )


@receiver(post_save, sender=VotingProcess)
def create_board_decision(sender, instance, created, **kwargs):
    logger.info(f"VotingProcess created ? {created}")
    if created:
        logger.info(
            f"Received post_save signal for VotingProcess with document_number: {instance.document_number}, status: "
            f"{instance.status}")

        try:
            if instance.status.lower() == ENDED.lower():
                logger.info(
                    f"VotingProcess with document_number {instance.document_number} has ended. Initiating board "
                    f"decision creation.")

                service = VotingDecisionManager(
                    document_number=instance.document_number,
                    board_meeting=instance.board_meeting,
                )
                service.create_board_decision()
            else:
                logger.info(
                    f"No action required for VotingProcess not ended. {instance.document_number}. {instance.status.lower()}")

        except SystemError as e:
            logger.error(
                f"SystemError: An error occurred while creating the board decision for document_number "
                f"{instance.document_number}. Error: {str(e)}"
            )
        except Exception as ex:
            logger.error(
                f"An unexpected error occurred while trying to create board decision for document_number "
                f"{instance.document_number}. Error: {str(ex)}",
                exc_info=True  # This will include the full stack trace in the log
            )
    else:
        logger.info(
            f"No action VotingProcess {instance.document_number}. {instance.status.lower()} vs {ENDED.lower()}")


@receiver(post_save, sender=BoardMeeting)
def update_meeting_votes(sender, instance, created, **kwargs):
    try:
        logger.info(f"Updating meeting votes for {instance.title}")
        if instance.status == CANCELLED:
            # Get the agenda of the meeting
            logger.info(f"Updating meeting status for {instance.status}")
            agenda = Agenda.objects.get(meeting=instance)
            if agenda:
                app_batch = agenda.application_batch
                app_batch.delete()
        # Update the votes of the meeting

    except Agenda.DoesNotExist:
        logger.warning("No agenda found for the canceled meeting.")

    except Exception as e:
        logger.error(f"Error handling cancelled meeting: {e}")


# Optionally, add a pre_delete signal to handle cascading deletion or updates if needed
@receiver(pre_delete, sender=ApplicationBatch)
def pre_delete_application_batch(sender, instance, **kwargs):
    # Update batched status to False for each application in the batch before deletion
    batched_apps = instance.applications.all()
    batched_apps.update(batched=False)


@receiver(post_save, sender=ApplicationBatch)
def update_application_batch(sender, instance, created, **kwargs):
    try:
        if created:
            # Update the batched status of the applications in the batch
            batched_apps = instance.applications.all()
            batched_apps.update(batched=True)
    except Exception as e:
        logger.error(f"Error updating application batch: {e}")
