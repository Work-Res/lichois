import logging
import base64

from django.db import transaction

from datetime import date

from app.api.common.web import APIMessage, APIResponse
from workresidentpermit.api.dto.permit_request_dto import PermitRequestDTO

from app_personal_details.models import Permit
from app_checklist.models import SystemParameter

from identifier.short_identifier import ShortIdentifier


class PermitProductionService:
    """Responsible for creating a new permit when production is accepted.
    """

    def __init__(self, request: PermitRequestDTO):
        self.request = request
        self.logger = logging.getLogger(__name__)
        self._systems_parameter = None
        self.response = APIResponse()

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.request.application_type
            )
        except SystemParameter.DoesNotExist:
            pass
        return self._systems_parameter

    def calculated_date_duration(self):
        """ Pending for system parameter from app checklist"""
        return date(2025, 1, 1)

    def _get_existing_permit(self):
        try:
            permit = Permit.objects.get(
                document_number=self.request.document_number
            )
        except Permit.DoesNotExist:
            self.logger.error("Permit does not exists")
            api_message = APIMessage(
                code=400,
                message="Permit does not exists.",
                details="Permit does not exists."
            )
            self.response.messages.append(api_message.to_dict())
        else:
            return permit

    def generate_security_number(self):
        short_identifier = ShortIdentifier(
            prefix_pattern='^[0-9]{10}$', prefix=24)
        self.request.permit_no = short_identifier.identifier
        encoded_data = base64.b64encode(self.request.permit_no)
        if len(encoded_data) > 8:
            code = encoded_data[:6]
            return code.upper()
        return encoded_data.upper()

    def generate_permint_number(self):
        return self.request.permit_no

    @transaction.atomic
    def create_new_permit(self):
        permit = self._get_existing_permit()
        if not permit:
            security_code = self.generate_security_number()
            Permit.objects.create(
                permit_type=self.request.permit_type,
                permit_no=self.request.permit_no,
                date_issued=self.request.date_issued or date.today(),
                date_expiry=self.calculated_date_duration(),
                place_issue=self.request.place_issue,
                security_number=security_code)

            api_message = APIMessage(
                code=200,
                message="Permit created successfully.",
                details="Permit created successfully."
            )
            self.response.status = "success"
            self.response.messages.append(api_message.to_dict())
        return permit

    def invalidate_existing_permit(self):
        pass
