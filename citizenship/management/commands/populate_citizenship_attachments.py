from django.core.management.base import BaseCommand
from app.models import ApplicationVerification, Application
from app_attachments.models import (
    ApplicationAttachment,
    ApplicationAttachmentVerification,
    AttachmentDocumentType,
)

from faker import Faker
from app_checklist.models import ChecklistClassifier, ChecklistClassifierItem
from authentication.models import User

APPLICATION_TYPES = [
    # "PRESIDENT_POWER_REGISTER_CITIZENS_10A"
    # "NATURALIZATION_INTENTION_FOREIGN_SPOUSE",
    "CITIZENSHIP_FOR_UNDER_20",
    # "MATURITY_PERIOD_WAIVER",
    # "RESUMPTION_OF_CITIZENSHIP",
    # "CITIZENSHIP_RENUNCIATION",

]


def is_pending_verification(application):
    """
    Checks if the application has a pending verification.

    :param application: Application instance.
    :return: True if pending verification exists, False otherwise.
    """
    return ApplicationVerification.objects.filter(
        document_number=application.application_document.document_number
    ).exists()


class Command(BaseCommand):
    help = "Populate data attachment for citizenship processes"

    def handle(self, *args, **options):
        faker = Faker()
        verifier = User.objects.filter(username="tverification1").first()

        if not verifier:
            self.stdout.write(
                self.style.ERROR("Verifier user 'tverification1' not found.")
            )
            return

        for application_type in APPLICATION_TYPES:

            applications = Application.objects.filter(process_name=application_type)
            _application_type = f"{application_type}_ATTACHMENT_DOCUMENTS"
            if not applications.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"No applications found for process: {application_type}"
                    )
                )
                continue

            classifier = ChecklistClassifier.objects.filter(
                code=_application_type
            ).first()
            if not classifier:
                self.stdout.write(
                    self.style.ERROR(
                        f"ChecklistClassifier with code '{application_type}' not found."
                    )
                )
                continue

            items = ChecklistClassifierItem.objects.filter(
                checklist_classifier=classifier
            )
            if not items.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"No ChecklistClassifierItems found for classifier: {application_type}"
                    )
                )
                continue

            for app in applications:
                if not is_pending_verification(app):
                    for item in items:
                        document_type, created = (
                            AttachmentDocumentType.objects.get_or_create(
                                code=item.code,
                                defaults={
                                    "name": item.name,
                                    "valid_to": faker.date_this_decade(),
                                    "valid_from": faker.date_this_decade()
                                },
                            )
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created new AttachmentDocumentType: {document_type.code}"
                                )
                            )

                        attachment = ApplicationAttachment.objects.create(
                            filename=faker.file_name(extension="pdf"),
                            storage_object_key=faker.uuid4(),
                            description=faker.sentence(),
                            document_url="https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf",
                            received_date=faker.date_time_this_decade(),
                            document_type=document_type,
                            document_number=app.application_document.document_number,
                        )

                        ApplicationAttachmentVerification.objects.create(
                            attachment=attachment,
                            verification_status="pending",
                            verifier=verifier,
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Populated data for application: {app.application_document.document_number}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Application {app} does not have pending verification."
                        )
                    )
