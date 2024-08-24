import logging


from django.db.models.signals import post_save
from django.dispatch import receiver

from app_assessment.models import AssessmentCaseDecision
from citizenship.exception import InterviewCompletionError
from citizenship.handlers.assessment_case_decision_post_save_handler import assessment_case_decision_post_save_handler
from citizenship.models import Interview
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from citizenship.service.handlers.postsave import InterviewCompletionHandler
from citizenship.service.handlers.postsave.conflict_duration_handler import ConflictDurationHandler

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AssessmentCaseDecision)
def assessment_case_decision_post_save(sender, instance, created, **kwargs):
    if created:
        assessment_case_decision_post_save_handler(sender, instance, created, **kwargs)


@receiver(post_save, sender=ConflictOfInterestDuration)
def handle_conflict_duration_completed(sender, instance, **kwargs):
    logger.info(f"Start process for creating interview responses.")
    handler = ConflictDurationHandler(conflict_duration=instance)
    handler.process()


@receiver(post_save, sender=Interview)
def handle_interview_status_change(sender, instance, **kwargs):
    """
    Signal handler to check and create scoresheet when interview status changes.
    """
    try:
        logger.info(f"Handling interview status change for Interview ID: {instance.id}, Status: {instance.status}")

        if instance.status == 'completed':
            logger.info(f"Interview ID: {instance.id} marked as completed. Initiating scoresheet creation.")
            handler = InterviewCompletionHandler(interview=instance)
            handler.check_and_create_scoresheet()
            logger.info(f"Scoresheet creation process completed for Interview ID: {instance.id}")
        else:
            logger.info(f"Interview ID: {instance.id} is not in a 'completed' status. No action taken.")

    except Exception as e:
        logger.error(f"Error handling interview status change for Interview ID: {instance.id}: {e}", exc_info=True)
