import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import (
    Application,
    CommissionerDecision,
    MinisterDecision,
    SecurityClearance,
)
from app.utils import ApplicationProcesses, ApplicationStatusEnum

from .classes import WorkPermitApplicationPDFGenerator
from .classes.config.configuration_loader import JSONConfigLoader
from .classes.service import (
    SpecialPermitDecisionService,
    WorkResidentPermitDecisionService,
)
from .classes.service.exemption_certification_decision_service import (
    ExemptionCertificateDecisionService,
)
from .models import WorkPermit

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@receiver(post_save, sender=WorkPermit)
def generate_pdf_summary(sender, instance, created, **kwargs):
    try:
        if sender.application_version.application.application_status.name in [
            ApplicationStatusEnum.VERIFICATION.value,
            ApplicationStatusEnum.CANCELLED.value,
            ApplicationStatusEnum.REJECTED.value,
            ApplicationStatusEnum.ACCEPTED.value,
        ]:
            generator = WorkPermitApplicationPDFGenerator(work_resident_permit=sender)
            generator.generate()
    except SystemError as e:
        logger.debug("SystemError: An error occurred while generating the PDF, Got ", e)
    except Exception as ex:
        logger.debug("An error occurred while generating the PDF, Got ", ex)


@receiver(post_save, sender=SecurityClearance)
def create_application_final_decision_by_security_clearance(
    sender, instance, created, **kwargs
):
    try:
        if created:
            try:
                application = Application.objects.get(
                    application_document__document_number=instance.document_number
                )
            except Application.DoesNotExist:
                logger.error(
                    f"Application not found for security clearance {instance.document_number}"
                )
                return
            else:
                if (
                    application.process_name.upper()
                    == ApplicationProcesses.WORK_RESIDENT_PERMIT.value
                ):
                    work_resident_permit_decision_service = (
                        WorkResidentPermitDecisionService(
                            document_number=instance.document_number,
                            security_clearance=instance,
                        )
                    )
                    work_resident_permit_decision_service.create_application_decision()
                elif (
                    application.process_name.upper()
                    == ApplicationProcesses.EXEMPTION_CERTIFICATE.value
                ):
                    exemption_certificate_decision_service = (
                        ExemptionCertificateDecisionService(
                            document_number=instance.document_number
                        )
                    )
                    exemption_certificate_decision_service.next_flow_activity()

    except SystemError as e:
        logger.error(
            "SystemError: An error occurred while creating new application decision, Got ",
            e,
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while trying to create application decision after saving board decision. "
            f"Got {ex} "
        )


def handle_application_final_decision(instance, created):

    json_file_name = "minister_approval_process.json"
    json_file_path = os.path.join(os.path.dirname(__file__), "data", json_file_name)

    config_loader = JSONConfigLoader(
        file_path=json_file_path, key="MINISTER_APPROVAL_PROCESSES"
    )
    if created:
        print("handle_application_final_decision created")
        try:
            special_permit_decision_service = SpecialPermitDecisionService(
                document_number=instance.document_number,
                config_loader=config_loader,
            )
            special_permit_decision_service.create_application_decision()
            logger.info("Application decision created successfully")
        except SystemError as e:
            logger.error(
                "SystemError: An error occurred while creating new application decision for "
                + f"{instance.document_number}, Got {e}"
            )
        except Exception as ex:
            logger.error(
                "An error occurred while trying to create application decision after saving "
                + f"{instance.document_number}. Got {ex}"
            )


@receiver(post_save, sender=CommissionerDecision)
def create_application_final_decision_by_commissioner_decision(
    sender, instance, created, **kwargs
):
    handle_application_final_decision(instance, created)


@receiver(post_save, sender=MinisterDecision)
def create_application_final_decision_by_minister_decision(
    sender, instance, created, **kwargs
):
    handle_application_final_decision(instance, created)
