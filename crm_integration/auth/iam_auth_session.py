import requests
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IAMAuthSession:
    def __init__(self, access_token: str, expires_in: str, refresh_expires_in: str, refresh_token: str):
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_expires_in = refresh_expires_in
        self.refresh_token = refresh_token
        self.expires_token_datetime = datetime.now() + timedelta(seconds=int(expires_in))
        self.refresh_token_datetime = datetime.now() + timedelta(seconds=int(refresh_expires_in))

    def get_access_token(self):
        return self.access_token

    def get_expires_token_datetime(self):
        return self.expires_token_datetime

    def get_refresh_token_datetime(self):
        return self.refresh_token_datetime

    def set_expires_token_datetime(self, expires_token_datetime: datetime):
        self.expires_token_datetime = expires_token_datetime

    def set_refresh_token_datetime(self, refresh_token_datetime: datetime):
        self.refresh_token_datetime = refresh_token_datetime
