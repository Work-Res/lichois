import logging
from datetime import datetime
from datetime import date

from app.models import SecurityClearance, Application
from app.service import BaseDecisionService

from app.workflow import GazetteTransactionData
from citizenship.utils import CitizenshipProcessEnum
from gazette.models import BatchApplication
from workflow.signals import create_or_update_task_signal

logger = logging.getLogger(__name__)


class GazetteCompletionService(BaseDecisionService):

    def __init__(self, batch_id):
        self.batch_id = batch_id
        self.workflow = GazetteTransactionData()
        self.document_number = None
        self.application = None
        self.security_clearance = None
        logger.info(f"GazetteCompletionService initialized with batch_id: {batch_id}")

    def _batch_applications(self):
        """Returns the batch applications for the given batch ID."""
        logger.debug(f"Fetching batch applications for batch_id: {self.batch_id}")
        return BatchApplication.objects.filter(batch__id=self.batch_id)

    def _get_security_clearance(self):
        """Fetches security clearance for the application if applicable."""
        if self.application and self.application.application_type == CitizenshipProcessEnum.NATURALIZATION.value:
            logger.debug(f"Attempting to fetch security clearance for document: {self.document_number}")
            try:
                security_clearance = SecurityClearance.objects.get(document_number=self.document_number)
                logger.info(f"Security clearance found for document {self.document_number}")
                return security_clearance
            except SecurityClearance.DoesNotExist:
                logger.warning(f"Security clearance pending for document {self.document_number}")
        return None

    def set_security_clearance(self):
        """Sets the security clearance for the workflow if available."""
        logger.debug(f"Setting security clearance for document {self.document_number}")
        self.security_clearance = self._get_security_clearance()
        if self.security_clearance:
            self.workflow.vetting_obj_exists = True
            logger.info(
                f"Security clearance set in workflow: {self.workflow.current_status} for document {self.document_number}"
            )

    def is_gazette_completed(self, batch_application):
        """Checks if the gazette process is completed based on the batch application."""
        gazette_completion_date = batch_application.batch.gazette_completion_date
        logger.debug(f"Checking if gazette is completed for batch application {batch_application.id}")
        if gazette_completion_date and date.today() > gazette_completion_date:
            logger.info(f"Gazette is completed for batch application {batch_application.id}")
            return True
        logger.info(f"Gazette is not yet completed for batch application {batch_application.id}")
        return False

    def set_gazette_batch_application(self, batch_application):
        """Sets gazette information in the workflow for a batch application."""
        logger.debug(f"Setting gazette status for batch application {batch_application.id}")
        self.workflow.gazette_completed = self.is_gazette_completed(batch_application)
        logger.info(
            f"Gazette status set in workflow {self.workflow.current_status} for document {self.document_number}"
        )

    def _activate_next_task(self, batch_application):
        """Activates the next workflow task for a batch application."""
        self.application = batch_application.application
        self.document_number = self.application.application_document.document_number
        logger.debug(f"Activating next task for document {self.document_number}")
        self.workflow.current_status = self.application.application_status.code.upper()
        # Set security clearance and gazette status
        self.set_security_clearance()
        self.set_gazette_batch_application(batch_application)

        # Trigger signal for the next task
        create_or_update_task_signal.send_robust(
            sender=self.application,
            source=self.workflow,
            application=self.application,
        )
        logger.info(f"Next task activated for document {self.document_number}")

    def activate_next_task_for_all(self):
        """Activates the next task for all batch applications."""
        logger.info(f"Activating next task for all applications in batch {self.batch_id}")
        batch_applications = self._batch_applications()

        if not batch_applications.exists():
            logger.warning(f"No batch applications found for batch_id: {self.batch_id}")

        for batch_application in batch_applications:
            try:
                self._activate_next_task(batch_application)
            except Exception as e:
                logger.error(
                    f"Failed to activate next task for batch application {batch_application.id}. Error: {e}",
                    exc_info=True
                )
