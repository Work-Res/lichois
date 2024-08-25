from django.test import TestCase

from django_mailbox.models import Mailbox, Message

from ..service.email_receiver.email_receiver_service import EmailReceiverService


class EmailReceiverServiceTest(TestCase):

    def setUp(self):
        pass
        # Setup the mailbox settings used by the EmailReceiverService
        self.mailbox_name = "Test Mailbox"
        # self.uri = "imap+ssl://test@example.com:password@mail.example.com"
        # self.from_email = "test@example.com"

        # Set these in the settings dictionary
        # self.settings = {
        #     "NAME": self.mailbox_name,
        #     "URI": self.uri,
        #     "FROM_EMAIL": self.from_email,
        # }

    def test_get_or_create_mailbox_new(self):
        # Act
        service = EmailReceiverService()

        # Assert
        mailbox = Mailbox.objects.get(name=self.mailbox_name)
        self.assertEqual(mailbox.uri, self.uri)
        self.assertEqual(mailbox.from_email, self.from_email)
        self.assertEqual(service.mailbox, mailbox)

    def test_get_or_create_mailbox_existing(self):
        # Arrange
        existing_mailbox = Mailbox.objects.create(
            name=self.mailbox_name,
            uri="imap+ssl://old@example.com:password@mail.example.com",
            from_email="old@example.com",
        )

        # Act
        service = EmailReceiverService()

        # Assert
        mailbox = Mailbox.objects.get(name=self.mailbox_name)
        self.assertEqual(mailbox.uri, self.uri)
        self.assertEqual(mailbox.from_email, self.from_email)
        self.assertEqual(service.mailbox, mailbox)
        self.assertEqual(mailbox.id, existing_mailbox.id)

    def test_fetch_unread_emails(self):
        # Arrange
        mailbox = Mailbox.objects.create(
            name=self.mailbox_name, uri=self.uri, from_email=self.from_email
        )
        message_1 = Message.objects.create(
            mailbox=mailbox, subject="Test 1", processed=None
        )
        message_2 = Message.objects.create(
            mailbox=mailbox, subject="Test 2", processed=None
        )
        message_3 = Message.objects.create(
            mailbox=mailbox, subject="Test 3", processed=None
        )

        service = EmailReceiverService()

        # Act
        unread_messages = service.fetch_unread_emails()

        # Assert
        self.assertEqual(len(unread_messages), 3)
        self.assertIn(message_1, unread_messages)
        self.assertIn(message_2, unread_messages)
        self.assertIn(message_3, unread_messages)

        # Verify that emails have been marked as read
        for message in unread_messages:
            self.assertIsNotNone(message.processed)
