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
    "WORK_PERMIT_ONLY",
    "WORK_PERMIT_EMERGENCY",
    "WORK_PERMIT_CANCELLATION",
    "WORK_PERMIT_REPLACEMENT",
    "WORK_PERMIT_APPEAL",
    "WORK_PERMIT_RENEWAL",
    "RESIDENT_PERMIT_ONLY",
    "RESIDENT_PERMIT_EMERGENCY",
    "RESIDENT_PERMIT_CANCELLATION",
    "RESIDENT_PERMIT_REPLACEMENT",
    "RESIDENT_PERMIT_APPEAL",
    "RESIDENT_PERMIT_RENEWAL",
    "WORK_RESIDENT_PERMIT_ONLY",
    "WORK_RESIDENT_PERMIT_EMERGENCY",
    "WORK_RESIDENT_PERMIT_EMERGENCY_REPLACEMENT",
    "WORK_RESIDENT_PERMIT_CANCELLATION",
    "WORK_RESIDENT_PERMIT_REPLACEMENT",
    "WORK_RESIDENT_PERMIT_APPEAL",
    "WORK_RESIDENT_PERMIT_RENEWAL",
    "EXEMPTION_CERTIFICATE_ONLY",
    "EXEMPTION_CERTIFICATE_APPEAL",
    "EXEMPTION_CERTIFICATE_CANCELLATION",
    "EXEMPTION_CERTIFICATE_REPLACEMENT",
    "EXEMPTION_CERTIFICATE_RENEWAL",
    "BLUE_CARD_ONLY",
    "BLUE_CARD_RETURNS",
    "BLUE_CARD_REPLACEMENT",
    "TRAVEL_CERTIFICATE",
    "PERMANENT_RESIDENCE_ONLY",
    "PERMANENT_RESIDENCE_10_YEARS",
    "VISA_PERMIT_ONLY",
    "WORK_RESIDENT_PERMIT_VARIATION",
    "WORK_PERMIT_VARIATION",
]


def is_pending_verification(application):
    """
    Checks if the application has a pending verification.
    """
    return ApplicationVerification.objects.filter(
        document_number=application.application_document.document_number
    ).exists()


class Command(BaseCommand):
    help = "Populate data attachment for work and res processes"

    def handle(self, *args, **options):
        faker = Faker()
        verifier = User.objects.filter(username="tverification1").first()

        if not verifier:
            verifier = User.objects.create_user(
                username="tverification1",
                email="tverification1@gmail.com",
                password="tverification1",
                first_name="Tverification",
                last_name="Tverification",
                is_staff=True,
                is_superuser=False,
            )

        for application_type in APPLICATION_TYPES:
            applications = Application.objects.filter(application_type=application_type)

            if not applications.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"No applications found for process: {application_type}"
                    )
                )
                continue

            classifier = ChecklistClassifier.objects.filter(
                code=f"{application_type}_ATTACHMENT_DOCUMENTS"
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
                                    "valid_from": faker.date_this_decade(),
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
                            f"Application {app.application_document.document_number} already has pending verification."
                        )
                    )
