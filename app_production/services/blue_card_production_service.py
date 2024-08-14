from datetime import date
import logging

from dateutil.relativedelta import relativedelta

from app_checklist.models.system_parameter import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from blue_card.enums import BlueCardApplicationTypeEnum

from ..api.dto.permit_request_dto import PermitRequestDTO


class BlueCardProductionService(PermitProductionService):

    application_type = BlueCardApplicationTypeEnum.BLUE_CARD_ONLY.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        self.request.permit_type = self.application_type

        super().__init__(request)

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.application_type
            )
            self.logger.info(
                f"System parameter found for {self.application_type}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.visa_type}, creating a new one."
            )
            self._systems_parameter = SystemParameter.objects.create(
                application_type=self.application_type,
                valid_from=date.today(),
                valid_to=date.today() + relativedelta(years=100),
                duration_type="years",
                duration=100,
            )
        return self._systems_parameter
