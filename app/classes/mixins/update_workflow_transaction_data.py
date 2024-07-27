import logging
from django.db import transaction
from rest_framework.exceptions import ValidationError
from app.models import Application
from app.workflow.transaction_data import BaseTransactionData


class UpdateApplicationMixin:

    def __init__(self, transaction_data: BaseTransactionData = None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @transaction.atomic
    def update_field(self, field_key, field_value):
        # Ensure the field_key is a valid field of the BaseTransactionData model
        if self.__getattribute__(field_key):
            self.__setattr__(field_key, field_value)
