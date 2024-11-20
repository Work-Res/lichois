from django.db.transaction import atomic
from app.models import Application
from authentication.models import User
from lichois.management.base_attachment_command import BaseAttachmentCommand
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(BaseAttachmentCommand):
    help = "Populate data attachments for multiple application types, each with its own checklist document"

    def handle(self, *args, **options):
        verifier = User.objects.filter(username="tverification1").first()

        if not verifier:
            self.stdout.write(
                self.style.ERROR(
                    "Verifier user 'tverification1' not found. Please create the user before running this command."
                )
            )
            return

        application_checklist_mapping = {
            WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_CANCELLATION.value: "RESIDENT_PERMIT_CANCELLATION_ATTACHMENT_DOCUMENTS",
            WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_CANCELLATION.value: "WORK_PERMIT_CANCELLATION_ATTACHMENT_DOCUMENTS",
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_CANCELLATION.value: "WORK_RESIDENT_PERMIT_CANCELLATION_ATTACHMENT_DOCUMENTS",
            WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_CANCELLATION.value: "EXEMPTION_CERTIFICATE_CANCELLATION_ATTACHMENT_DOCUMENTS",

        }

        with atomic():
            for application_type, checklist_code in application_checklist_mapping.items():
                self.handle_application_with_checklist(application_type, checklist_code, verifier)

            self.stdout.write(
                self.style.SUCCESS("Successfully processed all application types.")
            )

    def handle_application_with_checklist(self, application_type, checklist_code, verifier):
        """
        Processes applications of a specific type and associates them with their checklist items.
        """
        applications = Application.objects.filter(application_type=application_type)

        if not applications.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No applications found for process: {application_type}"
                )
            )
            return

        classifier = self.get_checklist_classifier(checklist_code)

        if not classifier:
            self.stdout.write(
                self.style.ERROR(f"ChecklistClassifier with code '{checklist_code}' not found.")
            )
            return

        items = self.get_checklist_items(classifier)

        if not items.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No ChecklistClassifierItems found for classifier: {checklist_code}"
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

    def get_checklist_classifier(self, checklist_code):
        """
        Retrieves the ChecklistClassifier for a given code.
        """
        from app_checklist.models import ChecklistClassifier
        return ChecklistClassifier.objects.filter(code=checklist_code).first()

    def get_checklist_items(self, classifier):
        """
        Retrieves items for a given checklist classifier.
        """
        from app_checklist.models import ChecklistClassifierItem
        return ChecklistClassifierItem.objects.filter(checklist_classifier=classifier)
