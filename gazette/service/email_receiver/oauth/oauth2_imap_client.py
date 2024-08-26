import logging
import imaplib
import base64

logger: logging.Logger = logging.getLogger(__name__)

from .token import get_oauth2_token

from django.conf import settings


class OAuth2IMAPClient:
    def __init__(self):
        self.client_id = settings.MS_CLIENT_ID
        self.client_secret = settings.MS_CLIENT_SECRET
        self.tenant_id = settings.MS_TENANT_ID
        self.email = settings.MS_EMAIL
        self.access_token = None

    def authenticate(self):
        # Implement the logic to get the access token
        logger.info("Authenticating to get the access token.")
        try:
            self.access_token = get_oauth2_token(
                self.client_id, self.client_secret, self.tenant_id
            )
            logger.info("Authentication successful.")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def connect(self):
        if not self.access_token:
            self.authenticate()

        auth_string = f"user={self.email}\1auth=Bearer {self.access_token}\1\1"
        auth_string = base64.b64encode(auth_string.encode("ascii")).decode("ascii")

        logger.info("Connecting to IMAP server...")

        try:
            mail = imaplib.IMAP4_SSL("outlook.office365.com")
            logger.info("Connected to IMAP server.")

            mail.authenticate("XOAUTH2", lambda x: auth_string)
            logger.info("Authenticated via XOAUTH2.")

            return mail
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise


# # Usage
# client = OAuth2IMAPClient(
#     client_id="your-client-id",
#     client_secret="your-client-secret",
#     tenant_id="your-tenant-id",
#     email="your-email@domain.com",
# )
# mail = client.connect()
