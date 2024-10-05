import logging

from app.models import Application
from app.utils import ApplicationDecisionEnum
from gazette.models import Batch
from gazette.service import ApplicationBatchService
from gazette.utils import GazetteConfiguration

from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError


class AddVettedApplicationToBatchService:
    def __init__(self, document_number):
        self.document_number = document_number
        self.logger = logging.getLogger(__name__)
        self.application = None

    def add_to_batch(self):
        try:
            # Retrieve the application
            self.application = self._get_application()
        except Application.DoesNotExist:
            self.logger.error(f"No Application found with document number: {self.document_number}")
            return
        except DatabaseError as e:
            # Handle database-related errors
            self.logger.critical(f"Database error while fetching application {self.document_number}: {e}", exc_info=True)
            return

        # Check eligibility and proceed to add to batch
        if self.is_eligible():
            try:
                batch = self.get_or_create_batch()
                if batch:
                    ApplicationBatchService.add_application_to_batch(batch.id, self.application.id)
                    self.application.gazette = ApplicationDecisionEnum.PENDING.value
                    self.application.save()
                    self.logger.info(f"Application {self.application.id} added to batch {batch.id}")
            except IntegrityError as e:
                self.logger.error(f"Integrity error while adding application {self.application.id} to batch: {e}", exc_info=True)
            except Exception as e:
                self.logger.error(f"Unexpected error while processing batch for application {self.application.id}: {e}", exc_info=True)
        else:
            self.logger.info(f"Application {self.document_number} is not eligible for gazetting.")

    def get_or_create_batch(self):
        try:
            counter = Batch.objects.count() + 1
            batch, created = Batch.objects.get_or_create_by_status(
                description=f"Batch {counter} created on {date.today()}",
                title=f"Batch {counter}"
            )
            if created:
                self.logger.info(f"New batch created with ID {batch.id}")
            return batch
        except DatabaseError as e:
            self.logger.error(f"Database error while creating or fetching batch: {e}", exc_info=True)
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error while creating or fetching batch: {e}", exc_info=True)
            return None

    def _get_application(self):
        # Retrieve application by document number, raise if not found
        try:
            return Application.objects.get(
                application_document__document_number=self.document_number
            )
        except ObjectDoesNotExist:
            raise Application.DoesNotExist(f"Application with document number {self.document_number} does not exist")
        except DatabaseError as e:
            self.logger.critical(f"Database error while retrieving application {self.document_number}: {e}",
                                 exc_info=True)
            raise

    def is_eligible(self):
        # Check eligibility based on process name
        process_name = self._get_process_name()
        if process_name in GazetteConfiguration.configured_process():
            self.logger.info(f"Application {self.application.id} is eligible with process name: {process_name}")
            return True
        self.logger.info(f"Application {self.application.id} is not eligible with process name: {process_name}")
        return False

    def _get_process_name(self):
        # Assume self.application is already set
        return self.application.process_name
