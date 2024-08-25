import logging
import os
from datetime import date

from app.utils.system_enums import ApplicationProcesses
from app_address.models.application_address import ApplicationAddress
from app_attachments.models.application_attachment import ApplicationAttachment
from app_personal_details.models.person import Person
from app_production.api.dto.permit_request_dto import PermitRequestDTO
from app_production.handlers.common.production_config import ProductionConfig
from app_production.handlers.common.production_context import GenericProductionContext
from app_production.handlers.postsave.upload_document_production_handler import (
    UploadDocumentProductionHandler,
)
from travel.models.travel_certificate import TravelCertificate

from .permit_production_service import PermitProductionService


class TravelCertificateProductionService(PermitProductionService):

    process_name = ApplicationProcesses.TRAVEL_CERTIFICATE.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        super().__init__(request)

    def create_new_permit(self):

        template_path = os.path.join(
            "travel",
            "data",
            "production",
            "templates",
            "travel_certificate_template.docx",
        )

        document_output_path_pdf = os.path.join(
            "travel", "data", "production", "output", "travel_certificate_output.pdf"
        )
        document_output_path_word = os.path.join(
            "travel", "data", "production", "output", "travel_certificate_output.docx"
        )
        config = ProductionConfig(
            template_path=template_path,
            document_output_path=document_output_path_word,
            document_output_path_pdf=document_output_path_pdf,
            is_required=True,
        )
        context = GenericProductionContext()
        context.context = lambda: self.get_context_data()

        handler = UploadDocumentProductionHandler()
        handler.execute(config_cls=config, production_context=context)
        self.logger.info(f"Document created for {self.request.document_number}")

    def get_tavel_certificate(self):
        try:
            return TravelCertificate.objects.get(
                document_number=self.request.document_number
            )
        except TravelCertificate.DoesNotExist:
            pass

    def get_personal_details(self):
        try:
            return Person.objects.get(document_number=self.request.document_number)
        except Person.DoesNotExist:
            pass

    def get_address_details(self):
        try:
            return ApplicationAddress.objects.get(
                document_number=self.request.document_number
            )
        except ApplicationAddress.DoesNotExist:
            pass

    def get_passport_photo(self):
        try:
            attachment = ApplicationAttachment.objects.get(
                document_number=self.request.document_number,
                document_type__code="passport_photo",
            )
            return attachment.document_url
        except ApplicationAttachment.DoesNotExist:
            return None

    def get_context_data(self):
        personal_details = self.get_personal_details()
        travel_certificate = self.get_tavel_certificate()
        data_context = {
            "surname": personal_details.last_name,
            "middle_name": personal_details.middle_name,
            "place_of_birth": personal_details.place_birth,
            "document_type": self.process_name.title(),
            "dob": str(personal_details.dob),
            "original_home_address": travel_certificate.original_home_address,
            "mother_full_names": travel_certificate.mother.full_name(),
            "mother_full_address": travel_certificate.mother_full_address,
            "chief": travel_certificate.chief_name,
            "country_of_origin": personal_details.country_birth,
            "present_nationality": personal_details.country_birth,
            "father_full_names": travel_certificate.father.full_name(),
            "father_full_address": travel_certificate.father_full_address,
            "names_of_other_living_relatives": travel_certificate.names_of_other_relatives,
            "full_address_of_relative": travel_certificate.full_address_of_relative,
            "kraal_head_or_headman": travel_certificate.kraal_head_name,
            "clan": travel_certificate.clan_name,
            "document_number": self.request.document_number,
            "date": str(date.today().strftime("%d %B %Y")),
            "year": str(date.today().year),
            "passport_photo": self.get_passport_photo(),
        }
        return data_context
