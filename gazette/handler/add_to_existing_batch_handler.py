from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import SecurityClearance
from gazette.service.batch_service import BatchService


@receiver(post_save, sender=SecurityClearance)
def handle_security_clearance_saved(sender, instance, created, **kwargs):
    batch_service = BatchService()

    if created:
        application = instance.application
        batch_service.logger.info(f"SecurityClearance created for Application {application.id}. "
                                  f"Initiating batch application process.")

        try:
            batch_service.create_batch_application(application)
            batch_service.logger.info(f"Successfully created batch application for Application {application.id}.")

        except Exception as e:
            batch_service.logger.error(f"Failed to create batch application for Application {application.id} "
                                       f"associated with SecurityClearance {instance.id}. Error: {str(e)}")
    else:
        batch_service.logger.info(f"SecurityClearance was updated, no batch application process triggered.")
