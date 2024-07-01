import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from board.choices import CANCELLED, ENDED
from board.classes.voting_decision_manager import VotingDecisionManager
from board.models import Agenda, ApplicationBatch, BoardDecision, BoardMeeting, VotingProcess

from workresidentpermit.classes.service import WorkResidentPermitDecisionService

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@receiver(post_save, sender=BoardDecision)
def create_application_decision(sender, instance, created, **kwargs):
    try:
        if created:
            work_resident_permit_decision_service = WorkResidentPermitDecisionService(
                document_number=instance.assessed_application.application_document.document_number,
                board_decision=instance
            )
            work_resident_permit_decision_service.create_application_decision()
            application = instance.assessed_application
            application.board = instance.decision_outcome
            application.save()
    except SystemError as e:
        logger.error("SystemError: An error occurred while creating new application decision, Got ", e)
    except Exception as ex:
        logger.error(f"An error occurred while trying to create application decision after saving board decision. "
                     f"Got {ex} ")


@receiver(post_save, sender=VotingProcess)
def create_board_decision(sender, instance, created, **kwargs):
    logger.info("instance status", instance.status)
    try:
        if instance.status == ENDED:
            service = VotingDecisionManager(
                document_number=instance.document_number,
                board_meeting=instance.board_meeting
            )
            board_decision = service.create_board_decision()
            print("board_decision", board_decision)
    except SystemError as e:
        logger.error("SystemError: An error occurred while creating new board decision, Got ", e)
    except Exception as ex:
        logger.error(f"An error occurred while trying to create board decision after saving voting process. "
                     f"Got {ex} ")


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
