from django_q.tasks import schedule

import logging

from gazette.service.email_receiver import EmailReceiverService

logger: logging.Logger = logging.getLogger(__name__)


def fetch_unread_emails_task():
    try:
        email_service = EmailReceiverService()
        unread_emails = email_service.fetch_unread_emails()
        logger.info(f"Fetched {len(unread_emails)} unread emails.")
    except Exception as e:
        logger.error(f"Failed to fetch unread emails: {e}")
