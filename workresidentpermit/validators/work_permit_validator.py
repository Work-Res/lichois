from app.api.common.web import APIMessage
from workresidentpermit.models import WorkPermit
from .work_resident_permit_validator import WorkResidentPermitValidator


class WorkPermitValidator(WorkResidentPermitValidator):

    """
    Responsible for validating all mandatory for work permit.
    """

    def find_missing_mandatory_fields(self):
        """
        Check if all required models are captured.
        """
        super().find_missing_mandatory_fields()

        try:
            WorkPermit.objects.get(document_number=self.document_number)
        except WorkPermit.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Work Permit Form is mandatory. ",
                    details=f"A work permit form is required to captured before submission."
                ).to_dict()
            )
