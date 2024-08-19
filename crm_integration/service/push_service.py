import os

import logging
import requests

from typing import List, Dict
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PushService:

    def __init__(self, config: Dict[str, str], iam_auth_connector):
        config = config or settings.crm_config
        self.crm_file_upload_url = config.get('CRM_FILE_UPLOAD_URL')
        self.crm_file_download_url = config.get('CRM_FILE_DOWNLOAD_URL')
        self.push_crm_url_prefix = config.get('PUSH_CRM_URL_PREFIX')
        self.push_crm_url_suffix = config.get('PUSH_CRM_URL_SUFFIX')
        self.push_crm_url = config.get('PUSH_CRM_URL')
        self.application_id_key = config.get('APPLICATION_ID_KEY')
        self.authorization_key = config.get('AUTHORISATION_KEY')
        self.notification_service = config.get('NOTIFICATION_SERVICE')
        self.file_dir = config.get('FILE_DIR')
        self.iam_auth_connector = iam_auth_connector

    def push_to_crm(self, push_request: dict, errors: Dict[str, List[str]]) -> dict:
        """
        Push data to the CRM system.

        Args:
            push_request (dict): The data to push to the CRM.
            errors (Dict[str, List[str]]): A dictionary to collect errors if the push fails.

        Returns:
            dict: The response from the CRM if successful.
            dict: A failure response with error details.
        """
        self.iam_auth_connector.manage_token()
        logger.info("Push request: %s", push_request)

        url = self._construct_url()
        headers = self._construct_headers()

        try:
            response = requests.post(url, json=push_request, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as ex:
            return self._handle_request_exception(ex, push_request, errors)

    def _construct_url(self) -> str:
        """Constructs the full URL for the CRM push."""
        return f"{self.push_crm_url_prefix}{self.notification_service}{self.push_crm_url_suffix}"

    def _construct_headers(self) -> Dict[str, str]:
        """Constructs the headers for the CRM push."""
        auth_session = self.iam_auth_connector.get_auth_session()
        return {
            'Content-Type': 'application/json',
            self.application_id_key: auth_session['session_state'],
            self.authorization_key: f"Bearer {auth_session['access_token']}"
        }

    def _handle_request_exception(self, ex: requests.exceptions.RequestException, push_request: dict,
                                  errors: Dict[str, List[str]]) -> dict:
        """Handles exceptions that occur during the CRM push."""
        logger.error("Error pushing to CRM: %s", ex)
        user_id = push_request.get('reference', {}).get('user_id')
        if user_id:
            errors.setdefault('NOTIFICATION', []).append(user_id)
        return {
            'success': False,
            'error': str(ex),
            'user_id': user_id
        }

    def upload_file(self, file_path: str) -> dict:
        """
        Uploads a file to the CRM system.

        Args:
            file_path (str): The path to the file that needs to be uploaded.

        Returns:
            dict: The response from the CRM as a JSON object if the upload is successful.

        Raises:
            FileNotFoundError: If the file does not exist at the given path.
            RuntimeError: If the upload fails due to a request exception or non-200 status code.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file at {file_path} was not found.")

        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(self.crm_file_upload_url, files=files)
                response.raise_for_status()
                # You a need strategy to store the upload attachment key

                logger.info(f"File uploaded successfully: {file_path}")
                return response.json()

        except requests.exceptions.RequestException as ex:
            logger.error(f"Error uploading file to {self.crm_file_upload_url}: {ex}")
            raise RuntimeError(f"Failed to upload file to CRM: {ex}") from ex

    def download_file(self, file_id: str, download_path: str):
        try:
            url = f"{self.crm_file_download_url}/{file_id}"
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(download_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        except requests.exceptions.RequestException as ex:
            logger.error("Error downloading file: %s", ex)
            raise
