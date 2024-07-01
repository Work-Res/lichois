import logging
import os

from django.conf import settings
from datetime import date

from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

from app_personal_details.models import Permit

logger = logging.getLogger(__name__)

# Fixme: NOT USED to consider deleting it..
class ProductionDocumentService:

    def __init__(self, document_number: str, permit_date=None, permit_type=None, place_issue=None):
        self.document_number = document_number
        self.permit_date = permit_date
        self.permit_type = permit_type
        self.place_issue = place_issue

    def upload_generated_pdf(self):
        file_name = f"{self.permit_date}_{self.document_number}.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, "generated", file_name)

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return

        try:
            with open(file_path, 'rb') as generated_pdf:
                permit_to_update = self.create_or_update_permit()
                permit_to_update.generated_pdf.save(file_name, File(generated_pdf))
                permit_to_update.save()
                logger.info(f"PDF {file_name} saved to Permit {permit_to_update.document_number}")
        except Exception as e:
            logger.error(f"Failed to read or save PDF: {e}")

    def create_or_update_permit(self):
        defaults = {
            "permit_type": self.permit_type,
            "permit_no": self.allocated_permit_number(),
            "date_issued": date.today(),
            "date_expiry": self.permit_duration_system_parameter(),
            "place_issue": self.place_issue
        }

        try:
            permit, created = Permit.objects.get_or_create(
                document_number=self.document_number,
                defaults=defaults
            )
            if not permit:
                logger.info(f"Permit with document number {self.document_number} already exists.")
                return created
            return permit
        except ObjectDoesNotExist as e:
            logger.error(f"Error creating or getting Permit: {e}")
            raise

    def allocated_permit_number(self):
        return "300000010"

    def permit_duration_system_parameter(self):
        return date(2025, 1, 1)
