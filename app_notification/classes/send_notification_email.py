import logging
from django.core.mail import EmailMessage, send_mail
from django_q.tasks import async_task

# Configure logging
from app_notification.models import Notification

logger = logging.getLogger(__name__)


def send_notification_email(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.user and notification.user.email:
            try:
                if notification.has_attachment:
                    # Dynamically fetch the attachment based on content_type and object_id
                    content_type = notification.content_type
                    model_class = content_type.model_class()
                    attachment = model_class.objects.get(id=notification.object_id)

                    email = EmailMessage(
                        'New Notification',
                        notification.message,
                        'from@example.com',
                        [notification.user.email]
                    )
                    email.attach_file(attachment.file.path)
                    email.send(fail_silently=False)
                else:
                    send_mail(
                        'New Notification',
                        notification.message,
                        'from@example.com',
                        [notification.user.email],
                        fail_silently=False,
                    )
                notification.is_read = True
                notification.save()
                logger.info(f'Notification {notification_id} sent to {notification.user.email}')
            except Exception as e:
                notification.retry_count += 1
                notification.save()
                logger.error(f'Error sending notification {notification_id} to {notification.user.email}: {e}')
                # Optionally, re-queue the task for retry if needed
                if notification.retry_count < 3:  # For example, retry up to 3 times
                    async_task('path.to.tasks.send_notification_email', notification_id)
    except Notification.DoesNotExist:
        logger.error(f'Notification with id {notification_id} does not exist')
    except Exception as e:
        logger.error(f'Unexpected error occurred while processing notification {notification_id}: {e}')
