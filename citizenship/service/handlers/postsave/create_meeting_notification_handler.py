import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from citizenship.models import Meeting
from citizenship.service.board import NotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Meeting)
def handle_meeting_notification_on_status_change(sender, instance, **kwargs):
    """
    Signal handler to create a meeting notification for the attendee.
    """
    logger.info(f"Handling status change for Meeting ID: {instance.id}, Status: {instance.status}")

    if instance.status == 'In_Preparation':
        try:
            with transaction.atomic():
                NotificationService.notify_attendees(meeting_id=instance.id)
                logger.info(f"Notification sent for Meeting ID: {instance.id}")
        except Exception as e:
            logger.error(f"Error sending notification for Meeting ID: {instance.id}: {e}")
