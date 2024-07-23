from django_q.tasks import async_task
from django.conf import settings

from django.core.mail import send_mail

from app_notification.models import Notification
from citizenship.models import Meeting, Attendee

from django.contrib.contenttypes.models import ContentType


class NotificationService:

    @staticmethod
    def create_notifications_for_attendees(meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        attendees = Attendee.objects.filter(meeting_id=meeting_id)

        for attendee in attendees:
            Notification.objects.create(
                user=attendee.member.user,
                content_type=ContentType.objects.get_for_model(meeting),
                object_id=meeting.id,
                message=f'A new meeting "{meeting.title}" has been scheduled on {meeting.date} at {meeting.time} in {meeting.location}.'
            )

    @staticmethod
    def send_email_notifications(meeting_id):
        attendees = Attendee.objects.filter(meeting_id=meeting_id)
        meeting = attendees.first().meeting
        subject = f'Notification for Meeting: {meeting.title}'
        message = f'A new meeting "{meeting.title}" has been scheduled on {meeting.date} at {meeting.time} in {meeting.location}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [attendee.member.user.email for attendee in attendees]

        send_mail(subject, message, from_email, recipient_list)

    @staticmethod
    def notify_attendees(meeting_id):
        NotificationService.create_notifications_for_attendees(meeting_id)
        async_task(NotificationService.send_email_notifications, meeting_id)
