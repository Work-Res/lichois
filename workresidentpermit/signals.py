import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Application, CommissionerDecision, MinisterDecision
from app.models.security_clearance import SecurityClearance
from app.utils import (
    ApplicationDecisionEnum,
    ApplicationProcesses,
    ApplicationStatusEnum,
)
from app_decision.models import ApplicationDecision
from workresidentpermit.api.dto.permit_request_dto import PermitRequestDTO
from workresidentpermit.classes.service import (
    PermitProductionService,
    SpecialPermitDecisionService,
    WorkResidentPermitDecisionService,
)
from workresidentpermit.models import WorkPermit

from .classes import WorkPermitApplicationPDFGenerator
from .classes.config.configuration_loader import JSONConfigLoader
from .classes.service.exemption_certification_decision_service import (
    ExemptionCertificateDecisionService,
)

logger = logging.getLogger(__name__)

logger.setLevel(logging.WARNING)

json_file_name = "approval_process.json"
json_file_path = os.path.join(os.path.dirname(__file__), "data", json_file_name)

logger.info(f"Loading approval process from {json_file_path}")
config_loader = JSONConfigLoader(
    file_path=json_file_path, key="MINISTER_APPROVAL_PROCESES"
)


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


# Assuming
# you have a
# ConfigurationLoader
# implementation


def handle_application_final_decision(instance, created):
    if not created:
        return
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


# TODO: Implement the signal receiver to create a production permit record after an application decision is saved.
# @receiver(post_save, sender=ApplicationDecision)
# def create_production_permit_record(sender, instance, created, **kwargs):
# 	"""Signal receiver to create a production permit record after an application decision is saved."""
# 	if not created:
# 		return
#
# 	# Create an instance of the service and handler
# 	permit_service = PermitProductionService(request=None)
# 	handler = ApplicationDecisionHandler(permit_service)
#
# 	# Handle the application decision
# 	handler.handle(instance)
@receiver(post_save, sender=ApplicationDecision)
def create_production_permit_record(sender, instance, created, **kwargs):
    print(
        "create_production_permit_record create_production_permit_record create_production_permit_record"
    )
    if not created:
        return
    try:
        if (
            instance.proposed_decision_type.code
            == ApplicationDecisionEnum.ACCEPTED.value
        ):
            request = PermitRequestDTO()
            application = Application.objects.get(
                application_document__document_number=instance.document_number
            )
            if application.process_name.upper() in [
                process_name.value.upper() for process_name in ApplicationProcesses
            ]:
                request.permit_type = application.process_name
                request.place_issue = "Gaborone"  # Pending location solution
                request.document_number = instance.document_number
                request.application_type = application.process_name
                permit = PermitProductionService(request=request)
                permit.create_new_permit()
    except SystemError as e:
        logger.error(
            f"SystemError: An error occurred while creating permit for production {instance.document_number}, Got {e}"
        )
    except Exception as ex:
        logger.error(
            f"An error occurred while trying to create permit for production {instance.document_number}. Got {ex}"
        )


# @receiver(post_save, sender=ApplicationDecision)
# def create_production_pdf(sender, instance, created, **kwargs):
#     try:
#         if created:
#             if instance.final_decision_type.code.lower() == ApplicationDecisionEnum.APPROVED.value.lower():
#                 async_production(document_number=instance.document_number)
#     except SystemError as e:
#         logger.error("SystemError: An error occurred while creating production pdf ", e)
#     except Exception as ex:
#         logger.error(f"An error occurred while trying to creating a production pdf "
#                      f"Got {ex} ")
