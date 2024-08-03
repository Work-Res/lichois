import logging
from app.models import Application

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ApplicationEligibilityValidator:

    def __init__(self, document_number):
        self.document_number = document_number

    def application(self):
        try:
            application = Application.objects.get(application_document__document_number=self.document_number)
            logger.debug("Found application: %s", application)
            return application
        except Application.DoesNotExist:
            logger.warning("No application found for document_number: %s", self.document_number)
            return None

    def is_valid(self):
        application = self.application()
        if application and not application.batched and self.has_completed_assessment():
            logger.debug("Application is valid: %s", application)
            return True
        logger.debug("Application is not valid: %s", application)
        return False

    def has_completed_assessment(self):
        # Assuming this method has more complex logic in the real scenario
        logger.debug("Checking if the assessment is completed for document_number: %s", self.document_number)
        return True