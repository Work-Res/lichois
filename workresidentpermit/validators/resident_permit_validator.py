from app.api.common.web import APIMessage
from workresidentpermit.models import ResidencePermit
from .work_resident_permit_validator import WorkResidentPermitValidator


class ResidentPermitValidator(WorkResidentPermitValidator):
    """
    Responsible for validating all mandatory for work permit.
    """

    def find_missing_mandatory_fields(self):
        """
        Check if all required models are captured.
        """
        super().find_missing_mandatory_fields()

        try:
            ResidencePermit.objects.get(document_number=self.document_number)
        except ResidencePermit.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Resident Permit Form is mandatory. ",
                    details="A work permit form is required to be captured before submission.",
                )
            )
