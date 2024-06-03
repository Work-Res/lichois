from app.api.common.web import APIMessage
from workresidentpermit.models import WorkPermit
from .work_resident_permit_validator import WorkResidentPermitValidator

from .work_permit_fields_validator import *


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
            self.work_permit = WorkPermit.objects.get(document_number=self.document_number)
        except WorkPermit.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Work Permit Form is mandatory. ",
                    details=f"A work permit form is required to captured before submission."
                ).to_dict()
            )

    def validate_form_fields(self):
        """
        Check if provided document is valid.
        """
        document_validator = DocumentNumberValidator({'document_number': self.document_number})
        if not document_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid document number data format ",
                    details=f"The specified document does not meet the required format, {self.document_number}"
                ).to_dict()
            )

        renumeration_validator = DecimalValidator({"decimal_value": self.work_permit.renumeration})
        if not renumeration_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid renumeration data format ",
                    details=f"The specified renumeration should be an decimal number only, {self.work_permit.renumeration}"
                ).to_dict()
            )

        period_permit_sought_validator = DigitsOnlyValidator({"value": self.work_permit.period_permit_sought})
        if not period_permit_sought_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid period_permit_sought data format ",
                    details=f"The specified period_permit_sought should be a digit data only, {self.work_permit.period_permit_sought}"
                ).to_dict()
            )

        no_bots_citizens_validator = DigitsOnlyValidator({"value": self.work_permit.no_bots_citizens})
        if not no_bots_citizens_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid number of botswana citizens data format ",
                    details=f"The specified number of Botswana citizens should be a digit data only, {self.self.work_permit.no_bots_citizens}"
                ).to_dict()
            )

        business_name_validator = TextFieldOnlyValidator({"name": self.work_permit.business_name})
        if not business_name_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid number of Business name data format ",
                    details=f"The specified number of business name should be a digit data only, {self.work_permit.business_name}"
                ).to_dict()
            )

        employer_validator = TextFieldOnlyValidator({"name": self.work_permit.employer})
        if not employer_validator.validate():
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid employer name data format ",
                    details=f"The specified employer name should be a digit data only, {self.work_permit.employer}"
                ).to_dict()
            )

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        super().validate()
        self.validate_form_fields()
        return True if len(self.response.messages) == 0 else False
