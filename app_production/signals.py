import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Application
from app.utils import ApplicationDecisionEnum
from app_decision.models import ApplicationDecision
from .api.dto.permit_request_dto import PermitRequestDTO
from .utils import get_service_registry


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@receiver(post_save, sender=ApplicationDecision)
def create_production_permit_record(sender, instance, created, **kwargs):
    if created:
        print("instance ", instance)
        try:
            if (
                instance.proposed_decision_type.code.upper()
                == ApplicationDecisionEnum.ACCEPTED.value.upper()
            ):
                request = PermitRequestDTO()
                application = Application.objects.get(
                    application_document__document_number=instance.document_number
                )

                request.document_number = instance.document_number
                request.application_type = application.application_type
                request.place_issue = "Gaborone"
                request.security_number = "123456"

                service_registry = get_service_registry()
                service_cls = service_registry.get_service(application.application_type)
                print("service_cls ", service_cls)
                service_cls(request).create_new_permit()

        except SystemError as e:
            logger.error(
                "SystemError: An error occurred while creating permit for production "
                + f"{instance.document_number}, Got {e}"
            )
        except Exception as ex:
            logger.error(
                f"An error occurred while trying to create permit for production {instance.document_number}. Got {ex}"
            )