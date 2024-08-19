import requests
from datetime import datetime, timedelta
import logging

from crm_integration.auth import IAMAuthSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IAMAuthConnector:
    def __init__(self, config: dict):
        self.auth_create_url = config['auth_create_url']
        self.auth_refresh_url = config['auth_refresh_url']
        self.username = config['username']
        self.password = config['password']
        self.refresh_key = config['refresh_key']
        self.iam_auth_session = None

    def manage_token(self):
        now = datetime.now()
        if self.iam_auth_session is None or now > self.iam_auth_session.get_refresh_token_datetime():
            self.create_token()
        elif now > self.iam_auth_session.get_expires_token_datetime() and \
                now < self.iam_auth_session.get_refresh_token_datetime():
            self.refresh_token()

    def create_token(self):
        try:
            response = requests.post(
                self.auth_create_url,
                json={'username': self.username, 'password': self.password},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            data = response.json()
            self.iam_auth_session = IAMAuthSession(
                access_token=data['access_token'],
                expires_in=data['expires_in'],
                refresh_expires_in=data['refresh_expires_in'],
                refresh_token=data['refresh_token']
            )
            logger.info("JWT Token: %s", self.iam_auth_session.get_access_token())
        except requests.exceptions.RequestException as e:
            logger.error("Error creating token: %s", e)
            raise

    def refresh_token(self):
        try:
            response = requests.post(
                self.auth_refresh_url,
                params={self.refresh_key: self.iam_auth_session.refresh_token},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            data = response.json()
            self.iam_auth_session = IAMAuthSession(
                access_token=data['access_token'],
                expires_in=data['expires_in'],
                refresh_expires_in=data['refresh_expires_in'],
                refresh_token=data['refresh_token']
            )
        except requests.exceptions.RequestException as e:
            logger.error("Error refreshing token: %s", e)
            raise
