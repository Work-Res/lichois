import logging
from app_address.models.application_address import ApplicationAddress
from app_personal_details.models.person import Person
from app_production.api.dto.permit_request_dto import PermitRequestDTO
from app_production.services import document
from travel.models.travel_certificate import TravelCertificate
from travel.utils import TravelCertificateEnum
from .permit_production_service import PermitProductionService


class TravelCertificateProductionService(PermitProductionService):

    application_type = TravelCertificateEnum.TRAVEL_CERTIFICATE.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        super().__init__(request)

    def create_permit(self):

        self.context = {
            "surname": "Letsile Tebogo",
            "middle_name": "Schoolboy",
            "place_of_birth": "Kanye",
            "document_type": "travel_certificate",
            "dob": "06/10/2003",
            "place_of_birth": "Kanye",
            "present_nationality": "Motswana",
            "original_home_address": "Ntsweng, Kanye",
            "mother_full_names": "Seritiwa Letsile",
            "mother_full_address": "Ntsweng, Kanye",
            "chief": "Thelekelo, Karabo",
            "country_of_origin": "Botswana",
            "father_full_names": "",
            "father_full_address": "",
            "names_of_other_living_relatives": "",
            "full_address_of_relative": "",
            "kraal_head_or_headman": "",
            "clan": "",
            "document_number": "TRC/010000",
            "date": "09/08/2024",
            "year": "2024",
        }

    def get_tavel_certificate_context(self):
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
