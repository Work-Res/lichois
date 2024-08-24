import logging
from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from gazette.models import Batch, BatchApplication


class BatchService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @transaction.atomic
    def get_or_create(self):
        date_string = date.today().strftime("%Y-%m-%d")
        batch_title = f"Batch {date_string}"
        batch_description = (
            f"Gazette batch list to reach maximum size: {settings.GAZETTE_BATCH_SIZE}"
        )

        try:
            # Attempt to create or get the batch
            batch, created = Batch.objects.get_or_create_by_status(
                status="OPEN",
                defaults={
                    "title": batch_title,
                    "description": batch_description,
                },
            )

            if created:
                self.logger.info(f"Successfully created new batch: {batch.title}")
            else:
                self.logger.info(
                    f"Successfully retrieved existing batch: {batch.title}"
                )

            return batch, created

        except IntegrityError as ie:
            self.logger.error(
                f"Integrity error while creating or retrieving batch: {ie}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during batch creation or retrieval: {e}"
            )
            raise

    @transaction.atomic
    def create_batch_application(self, application):
        if not self.is_eligible_for_gazetting(application):
            self.logger.warning(
                f"Application {application} is not eligible for gazetting."
            )
            return None

        try:
            batch, created = self.get_or_create()

            if batch.batch_applications.count() >= settings.GAZETTE_BATCH_SIZE:
                batch.status = "PENDING_SUBMISSION"
                batch.save()
                self.logger.info(
                    f"Batch {batch.title} reached maximum capacity, marked as PENDING_SUBMISSION."
                )
                return self.create_batch_application(application)

            batch_application = BatchApplication.objects.create(
                application=application, batch=batch
            )
            self.logger.info(f"Application {application} added to batch {batch.title}")
            return batch_application

        except ValidationError as error:
            self.logger.error(
                f"Validation error while creating batch application for {application}: {error}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error while creating batch application for {application}: {e}"
            )
            raise

    def is_eligible_for_gazetting(self, application):
        eligibility_criteria = []
        if application.application_type not in eligibility_criteria:
            self.logger.info(
                f"Application {application} is not eligible for gazetting based on type."
            )
            return False
        return True
