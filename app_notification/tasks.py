
from django_q.tasks import schedule, Schedule
from datetime import timedelta
from django.utils import timezone

from app_notification.classes.send_notification_email import send_notification_email
from app_notification.models import Notification


def send_unread_notifications():
    unread_notifications = Notification.objects.filter(is_read=False)
    for notification in unread_notifications:
        send_notification_email(notification)


# Schedule this task to run every hour
schedule(
    'app_notification.tasks.send_unread_notifications',
    schedule_type=Schedule.HOURLY,
    next_run=timezone.now() + timedelta(hours=1)
)
