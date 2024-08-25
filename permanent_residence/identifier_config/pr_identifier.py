from identifier.identifier import Identifier
from app.utils import ApplicationProcesses


class PermanentResidenceIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = (
        "permanentresidencepermit"  # e.g. work_permit_identifier, visa_identifier, etc
    )
    identifier_type = "PR"

    @staticmethod
    def process_name():
        return ApplicationProcesses.PERMANENT_RESIDENCE.value
