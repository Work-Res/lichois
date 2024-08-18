import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailNotificationService:

    @staticmethod
    def send_email_notifications(context, template_name, attachment_file_path=None):
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = context.get("to_email")
        subject = context.get("subject")

        try:
            html_message = render_to_string(f'emails/{template_name}', context)
            plain_message = strip_tags(html_message)

            email = EmailMessage(subject, plain_message, from_email, [to_email])
            email.content_subtype = 'html'
            email.attach_alternative(html_message, "text/html")

            # Attach the file if provided
            if attachment_file_path:
                email.attach_file(attachment_file_path)
                logger.info(f'Attachment {attachment_file_path} added to email for {to_email}')

            # Send the email
            email.send(fail_silently=False)
            logger.info(f'Email sent to {to_email} with subject "{subject}"')

        except Exception as e:
            logger.error(f'Error sending email to {to_email} with subject "{subject}": {e}')
            raise
