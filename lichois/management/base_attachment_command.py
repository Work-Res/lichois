from django.core.management.base import BaseCommand
from faker import Faker
from app.models import ApplicationVerification, Application
from app_attachments.models import (
    ApplicationAttachment,
    ApplicationAttachmentVerification,
    AttachmentDocumentType,
)
from app_checklist.models import ChecklistClassifier, ChecklistClassifierItem


class BaseAttachmentCommand(BaseCommand):
    faker = Faker()

    def is_pending_verification(self, application):
        """
        Checks if the application has a pending verification.
        """
        return ApplicationVerification.objects.filter(
            document_number=application.application_document.document_number
        ).exists()

    def handle_checklist_items(self, application, items, verifier):
        """
        Handles creating attachments for a given application and checklist items.
        """
        for item in items:
            document_type, created = AttachmentDocumentType.objects.get_or_create(
                code=item.code,
                defaults={
                    "name": item.name,
                    "valid_to": self.faker.date_this_decade(),
                    "valid_from": self.faker.date_this_decade(),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created new AttachmentDocumentType: {document_type.code}"
                    )
                )

            attachment = ApplicationAttachment.objects.create(
                filename=self.faker.file_name(extension="pdf"),
                storage_object_key=self.faker.uuid4(),
                description=self.faker.sentence(),
                document_url="https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf",
                received_date=self.faker.date_time_this_decade(),
                document_type=document_type,
                document_number=application.application_document.document_number,
            )

            ApplicationAttachmentVerification.objects.create(
                attachment=attachment,
                verification_status="pending",
                verifier=verifier,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Populated data for application: {application.application_document.document_number}"
            )
        )

    def handle_application_type(self, application_type, verifier):
        """
        Processes all applications of a specific type and handles checklist items.
        """
        applications = Application.objects.filter(application_type=application_type)

        if not applications.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No applications found for process: {application_type}"
                )
            )
            return

        classifier = ChecklistClassifier.objects.filter(
            code=f"{application_type}_ATTACHMENT_DOCUMENTS"
        ).first()

        if not classifier:
            self.stdout.write(
                self.style.ERROR(
                    f"ChecklistClassifier with code '{application_type}_ATTACHMENT_DOCUMENTS' not found."
                )
            )
            return

        items = ChecklistClassifierItem.objects.filter(
            checklist_classifier=classifier
        )

        if not items.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No ChecklistClassifierItems found for classifier: {application_type}"
                )
            )
            return

        for app in applications:
            if not self.is_pending_verification(app):
                self.handle_checklist_items(app, items, verifier)
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Application {app.application_document.document_number} already has pending verification."
                    )
                )
