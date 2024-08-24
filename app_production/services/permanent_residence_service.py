from datetime import date
import logging

from dateutil.relativedelta import relativedelta

from app.utils.system_enums import ApplicationProcesses
from app_checklist.models.system_parameter import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from permanent_residence.enums import PermanentResidenceApplicationTypeEnum

from ..api.dto.permit_request_dto import PermitRequestDTO


class PermanentResidenceProductionService(PermitProductionService):

    process_name = ApplicationProcesses.PERMANENT_RESIDENCE.value

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
                f"System parameter not found for {self.visa_type}, creating a new one."
            )

            duration = self.get_duration_and_validity()
            self._systems_parameter = SystemParameter.objects.create(
                application_type=self.request.permit_type,
                valid_from=date.today(),
                valid_to=date.today() + relativedelta(years=duration),
                duration_type="years",
                duration=duration,
            )
        return self._systems_parameter

    def get_duration_and_validity(self):
        return (
            10
            if self.request.permit_type
            == PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_10_YEARS
            else 100
        )
