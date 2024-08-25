from datetime import date
import logging

from dateutil.relativedelta import relativedelta

from app.utils.system_enums import ApplicationProcesses
from app_checklist.models.system_parameter import SystemParameter
from app_production.services.permit_production_service import PermitProductionService
from workresidentpermit.models.exemption_certificate import ExemptionCertificate
from workresidentpermit.models.work_permit import WorkPermit

from ..api.dto.permit_request_dto import PermitRequestDTO


class ExemptionCertificateProductionService(PermitProductionService):

    process_name = ApplicationProcesses.EXEMPTION_CERTIFICATE.value

    def __init__(self, request: PermitRequestDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request = request
        self.request.permit_type = self.process_name

        super().__init__(request)

    def systems_parameter(self):
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.process_name
            )
            self.logger.info(
                f"System parameter found for {self.process_name}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.process_name}, creating a new one."
            )
            self._systems_parameter = SystemParameter.objects.create(
                application_type=self.process_name,
                valid_from=date.today(),
                valid_to=date.today() + relativedelta(years=5),
                duration_type="years",
                duration=5,
            )
        return self._systems_parameter

    def get_exemption_certificate(self):
        try:
            exemption_certificate = ExemptionCertificate.objects.get(
                document_number=self.request.document_number
            )
            return exemption_certificate
        except ExemptionCertificate.DoesNotExist:
            return None
