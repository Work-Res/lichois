import logging

from dateutil.relativedelta import relativedelta

from app.utils.system_enums import ApplicationProcesses
from app_checklist.models.system_parameter import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from visa.models.visa_application import VisaApplication

from ..api.dto.permit_request_dto import PermitRequestDTO


class VisaProductionService(PermitProductionService):

    process_name = ApplicationProcesses.VISA_PERMIT.value

    def __init__(self, request: PermitRequestDTO):
        self.visa = self._get_visa_application(request.document_number)
        self.visa_type = f"{self.visa.visa_type} VISA".upper()
        request.permit_type = self.visa_type
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        super().__init__(request)

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.visa_type
            )
            self.logger.info(
                f"System parameter found for {self.visa_type}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.visa_type}, creating a new one."
            )
            key, value = self.calculated_date_duration()

            self._systems_parameter = SystemParameter.objects.create(
                application_type=self.visa_type,
                valid_from=self.visa.requested_valid_from,
                valid_to=self.visa.requested_valid_to,
                duration_type=key,
                duration=value,
            )
            self.logger.info("System parameter created successfully.")
        return self._systems_parameter

    def _get_visa_application(self, document_number):
        try:
            visa_application = VisaApplication.objects.get(
                document_number=document_number
            )
        except VisaApplication.DoesNotExist:
            return None
        return visa_application

    def calculated_date_duration(self):
        delta = relativedelta(
            self.visa.requested_valid_to, self.visa.requested_valid_from
        )
        years = delta.years
        months = delta.months
        weeks = delta.days // 7
        days = delta.days % 7

        if years:
            return "years", abs(years)
        elif months:
            return "months", abs(months)
        elif weeks:
            return "weeks", abs(weeks)
        elif days:
            return "days", abs(days)
