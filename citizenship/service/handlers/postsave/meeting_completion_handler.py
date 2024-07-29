import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from citizenship.models import Meeting, Interview, ScoreSheet

logger = logging.getLogger(__name__)


class MeetingCompletionHandler:
    @staticmethod
    def handle_meeting_completed(meeting):
        try:
            with transaction.atomic():
                # Get all meeting sessions related to this meeting
                meeting_sessions = meeting.sessions.all()

                # Iterate over each meeting session to get related interviews
                for session in meeting_sessions:
                    interviews = session.interviews.filter(status__in=['pending', 'in_progress'])

                    # Mark each interview and its score sheet as completed
                    for interview in interviews:
                        interview.status = 'completed'
                        interview.save()

                        # Mark the related score sheet as completed
                        try:
                            score_sheet = interview.score_sheet
                            score_sheet.status = 'completed'
                            score_sheet.save()
                        except ObjectDoesNotExist:
                            logger.warning(f"No score sheet found for interview {interview.id}")

                logger.info(f"All interviews and score sheets for meeting {meeting.id} marked as completed.")
        except Exception as e:
            logger.exception(f"Error updating interviews and score sheets for meeting {meeting.id}: {e}")


@receiver(post_save, sender=Meeting)
def handle_meeting_status_change(sender, instance, **kwargs):
    """
    Signal handler to mark related interviews and score sheets as completed when a meeting's status changes to completed.
    """
    if instance.status == 'completed':
        MeetingCompletionHandler.handle_meeting_completed(instance)