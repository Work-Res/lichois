import logging
import random
from datetime import date, datetime

from django.db import transaction

from app.api.common.web import APIMessage, APIResponse
from app_checklist.models import SystemParameter
from app_personal_details.models import Permit

from ..api.dto import PermitRequestDTO


class PermitProductionService:
    """Responsible for creating a new permit when production is accepted."""

    def __init__(self, request: PermitRequestDTO):
        self.request = request
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._systems_parameter = None
        self.response = APIResponse()

    def systems_parameter(self):
        try:
            print("self.request.application_type ", self.request.application_type)
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.request.application_type
            )
        except SystemParameter.DoesNotExist:
            pass
        return self._systems_parameter

    def _get_existing_permit(self):
        try:
            permit = Permit.objects.get(document_number=self.request.document_number)
        except Permit.DoesNotExist:
            pass
        else:
            return permit

    def generate_security_number(self):
        # try:
        self.request.permit_no = str(random.randint(320000000, 3399999999))
        #     encoded_data = base64.b64encode(self.request.permit_no)
        #     if len(encoded_data) > 8:
        #         code = encoded_data[:6]
        #         return code.upper()
        #     return encoded_data.upper()
        # except Exception as e:
        #     print(f"{e}")
        return self.request.permit_no

    def generate_permint_number(self):
        return self.request.permit_no

    @transaction.atomic
    def create_new_permit(self):
        permit = self._get_existing_permit()
        date_expiry = self.systems_parameter().valid_to
        if not permit:
            security_code = self.generate_security_number()
            Permit.objects.create(
                document_number=self.request.document_number,
                permit_type=self.request.permit_type,
                permit_no=self.request.permit_no,
                date_issued=self.request.date_issued or date.today(),
                date_expiry=date_expiry,
                place_issue=self.request.place_issue,
                security_number=security_code,
            )
            print(f"Permit created successfully for {self.request.document_number}")

            api_message = APIMessage(
                code=200,
                message="Permit created successfully.",
                details="Permit created successfully.",
            )
            self.response.status = "success"
            self.response.messages.append(api_message.to_dict())
            self.logger.info(
                f"Permit created successfully for {self.request.document_number}"
            )
        return permit

    def invalidate_existing_permit(self):
        pass

    def parse_iso_date(self, date_input):
        if not isinstance(date_input, str):
            raise ValueError("fromisoformat: argument must be str")
        return datetime.fromisoformat(date_input)
