import logging

from .classes import GenerateProductionPermitPDF
from django_q.tasks import async_task


logger = logging.getLogger(__name__)


def async_production(document_number: str):
    """
    Perform async on creating work permit pdf tasks.
    """
    pdf_util = GenerateProductionPermitPDF(document_number=document_number)
    task_id = async_task(pdf_util.pdf_generator)
    logger.info(f"The production generator is in progress for {document_number} with task id: {task_id}")
