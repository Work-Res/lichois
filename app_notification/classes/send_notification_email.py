import logging
from django_q.tasks import async_task

from app_notification.service import EmailNotificationService

logger = logging.getLogger(__name__)


class NotificationSender:
    def __init__(self, notification):
        self.notification = notification
        self.context = notification.context
        self.template_name = notification.template_name

    def send(self):
        if not self.notification:
            return

        if self.notification.user and self.notification.user.email:
            try:
                self.send_email(self.notification)
                self.mark_as_read(self.notification)
                logger.info(f'Notification {self.notification.id} sent to {self.notification.user.email}')
            except Exception as e:
                self.handle_send_error(self.notification, e)

    def send_email(self, notification):
        if notification.has_attachment:
            attachment = self.get_attachment(notification)
            EmailNotificationService.send_email_notifications(
                context=self.context,
                template_name=self.template_name,
                attachment_file_path=attachment.file.path if attachment else None
            )
        else:
            EmailNotificationService.send_email_notifications(
                context=self.context,
                template_name=self.template_name,
                attachment_file_path=None
            )

    def get_attachment(self, notification):
        try:
            content_type = notification.content_type
            model_class = content_type.model_class()
            return model_class.objects.get(id=notification.object_id)
        except Exception as e:
            logger.error(f'Error retrieving attachment for notification {self.notification_id}: {e}')
            return None

    def mark_as_read(self, notification):
        notification.is_read = True
        notification.save()

    def handle_send_error(self, notification, error):
        notification.retry_count += 1
        notification.save()
        logger.error(f'Error sending notification {self.notification_id} to {notification.user.email}: {error}')
        if notification.retry_count < 3:
            async_task('path.to.tasks.send_notification_email', self.notification_id)


def send_notification_email(notification):
    sender = NotificationSender(notification)
    try:
        sender.send()
    except Exception as e:
        logger.error(f'Error sending notification {notification.id}: {e}')
        notification.retry_count += 1
        notification.save()
        if notification.retry_count < 3:
            async_task('path.to.tasks.send_notification_email', notification.id)
