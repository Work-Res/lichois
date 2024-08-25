from django.conf import settings
from django_mailbox.models import Mailbox


class EmailReceiverService:
    def __init__(self):
        self.mailbox_name = settings.EMAIL_RECEIVER_SERVICE["NAME"]
        self.uri = settings.EMAIL_RECEIVER_SERVICE["URI"]
        self.from_email = settings.EMAIL_RECEIVER_SERVICE["FROM_EMAIL"]
        self.mailbox = self._get_or_create_mailbox()

    def _get_or_create_mailbox(self):
        mailbox, created = Mailbox.objects.get_or_create(
            name=self.mailbox_name,
            defaults={
                "uri": self.uri,
                "from_email": self.from_email,
            },
        )

        if not created:
            mailbox.uri = self.uri
            mailbox.from_email = self.from_email
            mailbox.save()

        return mailbox

    def fetch_unread_emails(self):
        """
        Fetch unread emails from the mailbox, mark them as read, and return their content.
        """
        # Fetch new emails marked as unseen (unread)
        messages = self.mailbox.get_new_mail(filters={"unseen": True})

        # Mark emails as read after fetching
        for message in messages:
            # Mark email as read
            message.mailbox.mark_as_seen(message)

            # Email is automatically saved to the Message model by django-mailbox
            print(f"Email with subject '{message.subject}' stored in the database.")

        return messages
