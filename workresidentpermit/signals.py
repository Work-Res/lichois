import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from workresidentpermit.models import WorkPermit
from app.utils import ApplicationStatuses

from .classes import WorkPermitApplicationPDFGenerator


@receiver(post_save, sender=WorkPermit)
def generate_pdf_summary(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    try:
        if sender.application_version.application.application_status.name in \
                [ApplicationStatuses.VERIFICATION.value,
                 ApplicationStatuses.CANCELLED.value,
                 ApplicationStatuses.REJECTED.value,
                 ApplicationStatuses.ACCEPTED.value]:
            generator = WorkPermitApplicationPDFGenerator(work_resident_permit=sender)
            generator.generate()
            # TODO post to SOLR
    except SystemError as e:
        logger.debug("SystemError: An error occurred while generating the PDF, Got ", e)
    except Exception as ex:
        logger.debug("An error occurred while generating the PDF, Got ", ex)
