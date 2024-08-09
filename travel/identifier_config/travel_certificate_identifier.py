from identifier.identifier import Identifier

from app.utils import ApplicationProcesses
from travel.utils import TravelCertificateEnum


class TravelCertificate(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "travelcertificate"
    identifier_type = "TC"

    @staticmethod
    def process_name():
        return ApplicationProcesses.TRAVEL_CERTIFICATE.value
