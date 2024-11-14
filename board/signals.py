import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from board.choices import CANCELLED, ENDED
from board.classes.voting_decision_manager import VotingDecisionManager
from .models import (
    Agenda,
    ApplicationBatch,
    BoardDecision,
    BoardMeeting,
    VotingProcess,
    Board,
    MeetingAttendee,
    MeetingInvitation,
)

from workresidentpermit.classes.service import WorkResidentPermitDecisionService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@receiver(post_save, sender=BoardDecision)
def create_application_decision(sender, instance, created, **kwargs):
    try:
        if created:
            logger.info(
                f"Creating application decision for document_number: {instance.document_number}"
            )
            work_resident_permit_decision_service = WorkResidentPermitDecisionService(
                document_number=instance.document_number,
                board_decision=instance,
            )
            work_resident_permit_decision_service.create_application_decision()
            work_resident_permit_decision_service.update_application()
            logger.info(
                f"Successfully created and updated application decision for document_number: {instance.document_number}"
            )
        else:
            logger.info(
                f"BoardDecision: No action required for document_number: {instance.document_number}"
            )
    except SystemError:
        logger.error(
            f"SystemError: An error occurred while creating new application decision"
            f"for document_number: {instance.document_number}",
            exc_info=True,
        )
    except Exception:
        logger.error(
            f"An unexpected error occurred while trying to create application decision"
            f"for document_number: {instance.document_number}",
            exc_info=True,  # Logs the full stack trace for any other exception
        )


@receiver(post_save, sender=VotingProcess)
def create_board_decision(sender, instance, created, **kwargs):
    logger.info(f"VotingProcess created ? {created}")
    if not created:
        logger.info(
            f"Received post_save signal for VotingProcess with document_number: {instance.document_number}, status: "
            f"{instance.status}"
        )

        try:
            if instance.status.lower() == ENDED.lower():
                logger.info(
                    f"VotingProcess with document_number {instance.document_number} has ended. Initiating board "
                    f"decision creation."
                )

                service = VotingDecisionManager(
                    document_number=instance.document_number,
                    board_meeting=instance.board_meeting,
                )
                service.create_board_decision()
            else:
                logger.info(
                    f"No action required for VotingProcess not ended. "
                    f"{instance.document_number}. {instance.status.lower()}"
                )

        except SystemError as e:
            logger.error(
                f"SystemError: An error occurred while creating the board decision for document_number "
                f"{instance.document_number}. Error: {str(e)}"
            )
        except Exception as ex:
            logger.error(
                f"An unexpected error occurred while trying to create board decision for document_number "
                f"{instance.document_number}. Error: {str(ex)}",
                exc_info=True,  # This will include the full stack trace in the log
            )
    else:
        logger.info(
            f"No action VotingProcess {instance.document_number}. {instance.status.lower()} vs {ENDED.lower()}"
        )


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


@receiver(
    post_save,
    weak=False,
    sender=BoardMeeting,
    dispatch_uid="board_meeting_on_post_save",
)
def board_meeting_on_post_save(sender, instance, raw, created, **kwargs):
    """Create board meeting invitations for all board members when a new board meeting is created."""
    if created and instance.status == "scheduled":
        board_id = instance.board_id
        board_members = None

        try:
            attending_board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return None
        else:
            board_members = attending_board.boardmember_set.all()
            for board_member in board_members:
                # Create a meeting invitation for each board member
                MeetingInvitation.objects.create(
                    board_meeting=instance,
                    invited_user=board_member,
                )
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


@receiver(
    post_save,
    weak=False,
    sender=MeetingInvitation,
    dispatch_uid="board_meeting_invitation_on_post_save",
)
def board_meeting_invitation_on_post_save(sender, instance, raw, created, **kwargs):
    if not created:
        attendance_status = "present" if instance.status == "approved" else "absent"

        # Check if a MeetingAttendee object with the given meeting_id and board_member_id already exists
        attendee_exists = MeetingAttendee.objects.filter(
            meeting=instance.board_meeting, board_member=instance.invited_user
        ).exists()

        if not attendee_exists:
            # If it doesn't exist, create a new one
            MeetingAttendee.objects.create(
                meeting=instance.board_meeting,
                board_member=instance.invited_user,
                attendance_status=attendance_status,
            )
        else:
            # If it does exist, update it
            MeetingAttendee.objects.filter(
                meeting=instance.board_meeting, board_member=instance.invited_user
            ).update(attendance_status=attendance_status)
