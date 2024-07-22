import logging

import time

from .classes import GenerateProductionPermitPDF
from django_q.tasks import async_task
from .classes.production import ProductionDocumentService

logger = logging.getLogger(__name__)


def async_production(document_number: str, application):
    """
    Perform async on creating work permit pdf tasks.
    """
    pdf_util = GenerateProductionPermitPDF(document_number=document_number)
    task_id = async_task(pdf_util.pdf_generator)

    time.sleep(
        3
    )  # temporarily pause, TODO: consider using scheduler..for uploading pdfs

    document_service = ProductionDocumentService(
        document_number=document_number, permit_type=application.application_type
    )
    document_service.upload_generated_pdf()

    logger.info(
        f"The production generator is in progress for {document_number} with task id: {task_id}"
    )
