import logging
import os

from django_q.tasks import async_task
from django.conf import settings

from django.core.mail import send_mail

from app_contact.models import ApplicationContact
from app_notification.models import Notification
from citizenship.models import Meeting, Attendee, BatchApplication

from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class NotificationService:

    @staticmethod
    def create_notifications_for_interviewees(meeting_id):
        footer_image = os.path.join(settings.BASE_DIR, 'media')
        meeting = Meeting.objects.get(id=meeting_id)
        batch_applications = BatchApplication.objects.filter(
            meeting_session__meeting=meeting
        )

        for batch_application in batch_applications:
            application = batch_application.application
            application_contact = ApplicationContact.objects.get(
                document_number=application.application_document.document_number,
                contact_type="email",
                preferred_method_comm=True
            )
            meeting_session = batch_application.meeting_session

            context = {
                "to_email": application_contact.contact_value,
                "interview_date": meeting_session.date,
                "Time": meeting_session.start_time,
                "Location": meeting.location,
                "Duration": meeting_session.get_duration(),
                "subject": f"Citizenship Application Interview Invitation - {meeting_session.date}",
                "footer_image": os.path.join(footer_image, "image_footer.png")
            }

            Notification.objects.create(
                content_type=ContentType.objects.get_for_model(meeting),
                object_id=meeting_session.id,
                message="",
                template_name="interview_invitation.html",
                context=context
            )

    @staticmethod
    def create_notifications_for_attendees(meeting_id):

        try:
            meeting = Meeting.objects.get(id=meeting_id)
            logger.info(f'Creating notifications for meeting ID: {meeting_id}, Title: {meeting.title}')
        except Meeting.DoesNotExist:
            logger.error(f'Meeting with ID {meeting_id} does not exist')
            return
        except Exception as e:
            logger.error(f'Unexpected error occurred while retrieving meeting with ID {meeting_id}: {e}')
            return

        try:
            attendees = Attendee.objects.filter(meeting_id=meeting_id)
            logger.info(f'Found {attendees.count()} attendees for meeting ID: {meeting_id}')
        except Exception as e:
            logger.error(f'Error retrieving attendees for meeting ID {meeting_id}: {e}')
            return
        footer_image = os.path.join(settings.BASE_DIR, 'media', "footer_image.png")
        for attendee in attendees:
            context = {
                "user": "",
                "footer_image": footer_image,
                "meeting_title": meeting.title,
                "meeting_start_date": meeting.start_date.strftime("%Y-%m-%d"),
                "meeting_end_date": meeting.end_date.strftime("%Y-%m-%d"),
                "to_email": attendee.member.user.email
            }
            try:
                Notification.objects.create(
                    user=attendee.member.user,
                    content_type=ContentType.objects.get_for_model(meeting),
                    object_id=meeting.id,
                    context=context,
                    template_name="interview_invitation.html"
                )
                logger.info(f'Notification created for user {attendee.member.user.email} for meeting ID: {meeting_id}')
            except Exception as e:
                logger.error(f'Error creating notification for user {attendee.member.user.email} for meeting ID {meeting_id}: {e}')


    @staticmethod
    def notify_attendees(meeting_id):
        NotificationService.create_notifications_for_attendees(meeting_id)
        async_task(NotificationService.send_email_notifications, meeting_id)
