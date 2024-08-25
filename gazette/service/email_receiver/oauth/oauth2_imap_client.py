import imaplib
import base64

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
        self.access_token = get_oauth2_token(
            self.client_id, self.client_secret, self.tenant_id
        )

    def connect(self):
        if not self.access_token:
            self.authenticate()

        auth_string = f"user={self.email}\1auth=Bearer {self.access_token}\1\1"
        auth_string = base64.b64encode(auth_string.encode("ascii")).decode("ascii")

        mail = imaplib.IMAP4_SSL("outlook.office365.com")
        mail.authenticate("XOAUTH2", lambda x: auth_string)
        return mail


# # Usage
# client = OAuth2IMAPClient(
#     client_id="your-client-id",
#     client_secret="your-client-secret",
#     tenant_id="your-tenant-id",
#     email="your-email@domain.com",
# )
# mail = client.connect()
