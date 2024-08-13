from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.application import Application
from app.models.application_verification import ApplicationVerification
from app.utils.system_enums import ApplicationProcesses
from travel.services.travel_certificate_decision_service import (
    TravelCertificateDecisionService,
)


@receiver(post_save, sender=ApplicationVerification)
def create_app_verification_signal(sender, instance, created, **kwargs):
    if created:
        try:
            application = Application.objects.get(
                application_document__document_number=instance.document_number
            )
        except Application.DoesNotExist:
            return
        else:
            if (
                application.process_name.upper()
                == ApplicationProcesses.TRAVEL_CERTIFICATE.value
            ):
                TravelCertificateDecisionService(
                    document_number=instance.document_number,
                    decision_value=instance.status.code,
                    application=application,
                ).create_application_decision()
