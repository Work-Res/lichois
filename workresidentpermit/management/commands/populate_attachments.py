from audioop import add
import random

from django.core.management.base import BaseCommand
from app.models import ApplicationDocument, ApplicationVerification
from app.models.application import Application
from app.utils.system_enums import ApplicationProcesses
from app_attachments.models import (
    ApplicationAttachment,
    ApplicationAttachmentVerification,
    AttachmentDocumentType,
)
from faker import Faker
from random import randint

from authentication.models import User


class Command(BaseCommand):
    help = "Populate data for Work & Res Application model"

    def add_arguments(self, parser):
        parser.add_argument(
            "application_process",
            type=str,
            help="Create system classifier for document types",
        )

    def handle(self, *args, **options):

        parameter = options["application_process"]
        if not parameter:
            raise ValueError("Please provide a valid process name")
        faker = Faker()
        apps = Application.objects.filter(process_name__iexact=parameter)
        verifier = User.objects.filter(username="tverification1").first()
        for app in apps:
            application = ApplicationVerification.objects.filter(
                document_number=app.application_document.document_number
            )
            if not application.exists():
                for _ in range(randint(0, 2) + 1):
                    document_type = AttachmentDocumentType.objects.create(
                        code=faker.random_int(min=1000, max=9999),
                        name=faker.random_element(
                            elements=(
                                "passport",
                                "national_id",
                                "birth_certificate",
                                "copy_work_permit",
                                "offer_letter",
                                "covering_letter",
                            )
                        ),
                        valid_from=faker.date_this_decade(),
                        valid_to=faker.date_this_decade(),
                    )
                    attachment = ApplicationAttachment.objects.create(
                        filename=faker.file_name(),
                        storage_object_key=faker.file_name(),
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

    def get_random_file_extension(self, category):
        file_extensions = {
            "pdf": [".pdf"],
            "image": [".jpg", ".png", ".gif"],
            "text": [".txt", ".doc", ".docx"],
            # Add more categories and file extensions as needed
        }

        return random.choice(file_extensions.get(category, []))
