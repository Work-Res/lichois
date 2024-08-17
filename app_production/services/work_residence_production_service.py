from datetime import date
import logging

from dateutil.relativedelta import relativedelta

from app.utils.system_enums import ApplicationProcesses
from app_checklist.models.system_parameter import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from workresidentpermit.models.work_permit import WorkPermit

from ..api.dto.permit_request_dto import PermitRequestDTO


class WorkResidenceProductionService(PermitProductionService):

    process_name = ApplicationProcesses.WORK_RESIDENT_PERMIT.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        self.request.permit_type = request.permit_type or self.process_name

        super().__init__(request)

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.request.application_type
            )
            self.logger.info(
                f"System parameter found for {self.request.application_type}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.request.application_type}, creating a new one."
            )
            self._systems_parameter = SystemParameter.objects.create(
                application_type=self.request.application_type,
                valid_from=date.today(),
                valid_to=date.today() + relativedelta(years=3),
                duration_type="years",
                duration=100,
            )
        return self._systems_parameter
