import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


from app.models import Application
from authentication.models import User
from gazette.exceptions import (
    BatchNotFoundException,
    ApplicationNotFoundException,
    BatchApplicationNotFoundException,
)

from gazette.models import Batch, BatchApplication

logger = logging.getLogger(__name__)


class ApplicationBatchService:

    @staticmethod
    @transaction.atomic
    def create_batch(title, description, created_by):
        try:
            batch = Batch.objects.create(title=title, description=description)
            logger.info(f"Batch created with ID {batch.id}")
            return batch
        except ObjectDoesNotExist as e:
            logger.error(f"User with ID {created_by} does not exist: {str(e)}")
            raise ValueError(f"User does not exist: {str(e)}")

    @staticmethod
    @transaction.atomic
    def add_application_to_batch(batch_id, application_id):
        try:
            batch = Batch.objects.get(id=batch_id)
            application = Application.objects.get(id=application_id)
            BatchApplication.objects.create(batch=batch, application=application)
            logger.info(
                f"Application with ID {application_id} added to batch with ID {batch_id}"
            )
        except ObjectDoesNotExist as e:
            if "Batch" in str(e):
                logger.error(f"Batch with ID {batch_id} does not exist")
                raise BatchNotFoundException()
            elif "Application" in str(e):
                logger.error(f"Application with ID {application_id} does not exist")
                raise ApplicationNotFoundException()

    @staticmethod
    @transaction.atomic
    def remove_application_from_batch(batch_id, application_id):
        try:
            batch_application = BatchApplication.objects.get(
                batch_id=batch_id, application_id=application_id
            )
            batch_application.delete()
            logger.info(
                f"Application with ID {application_id} removed from batch with ID {batch_id}"
            )
        except ObjectDoesNotExist as e:
            logger.error(
                f"BatchApplication with batch ID {batch_id} and application ID {application_id} does not exist"
            )
            raise BatchApplicationNotFoundException()

    @staticmethod
    @transaction.atomic
    def add_applications_to_batch(batch_id, application_ids):
        try:
            batch = Batch.objects.get(id=batch_id)
            applications = Application.objects.filter(id__in=application_ids)

            if len(applications) != len(application_ids):
                missing_ids = set(application_ids) - set(
                    applications.values_list("id", flat=True)
                )
                logger.error(f"Applications with IDs {missing_ids} do not exist")
                raise ApplicationNotFoundException(
                    f"Applications with IDs {missing_ids} do not exist"
                )

            for application in applications:
                BatchApplication.objects.create(batch=batch, application=application)
                logger.info(
                    f"Application with ID {application.id} added to batch with ID {batch_id}"
                )
        except ObjectDoesNotExist as e:
            if "Batch" in str(e):
                logger.error(f"Batch with ID {batch_id} does not exist")
                raise BatchNotFoundException()
            elif "Application" in str(e):
                logger.error(f"Application(s) with IDs {application_ids} do not exist")
                raise ApplicationNotFoundException()
