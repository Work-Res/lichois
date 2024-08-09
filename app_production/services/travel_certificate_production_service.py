import logging
from travel.utils import TravelCertificateEnum
from .permit_production_service import PermitProductionService


class TravelCertificateProductionService(PermitProductionService):

    application_type = TravelCertificateEnum.TRAVEL_CERTIFICATE.value

    def __init__(self, travel_certificate_repository):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def create_travel_certificate(self, travel_certificate):
        self.travel_certificate_repository.create(travel_certificate)
