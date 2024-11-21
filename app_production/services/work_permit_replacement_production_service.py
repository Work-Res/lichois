import logging

from app.utils import ApplicationProcesses
from app_checklist.models import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from citizenship.utils import CitizenshipProcessEnum

from ..api.dto.permit_request_dto import PermitRequestDTO


class WorkPermitReplacementProductionService(PermitProductionService):

    process_name = ApplicationProcesses.WORK_PERMIT_REPLACEMENT.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        self.request.permit_type = request.permit_type or self.process_name

        super().__init__(request)

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.request.permit_type
            )
            self.logger.info(
                f"System parameter found for {self.request.application_type}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.process_name}, creating a new one."
            )
        return self._systems_parameter

    def allowed_to_generate_document(self):
        self.logger.debug(f"{self.process_name} is configured to generate document for {self.request.document_number}")
        return True

    def is_allowed_create_dependent_permits(self):
        return True

