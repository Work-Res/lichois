from gazette.service.add_vetted_application_to_batch_service import AddVettedApplicationToBatchService
from ..api.dto import SecurityClearanceRequestDTO
from ..api.serializers import SecurityClearanceSerializer
from ..models import SecurityClearance
from ..service import BaseDecisionService
from ..utils.system_enums import ApplicationStatusEnum
from ..workflow.transaction_data import VettingTransactionData


class SecurityClearanceService(BaseDecisionService):
    def __init__(self, security_clearance_request: SecurityClearanceRequestDTO):
        workflow = VettingTransactionData(
            vetting_decision=security_clearance_request.status.upper(),
            vetting_obj_exists=True,
        )

        super().__init__(
            request=security_clearance_request,
            application_field_key="security_clearance",
            task_to_deactivate=ApplicationStatusEnum.VETTING.value,
            workflow=workflow,
        )

    def create_clearance(self):
        security_clearance = self.create_decision(SecurityClearance, SecurityClearanceSerializer)
        self.add_to_gazette_if_eligible(security_clearance)
        return security_clearance

    def add_to_gazette_if_eligible(self, security_clearance):
        document_number = security_clearance.get('data').get("document_number")
        self.logger.info(f"Start gazette process {document_number}")
        service = AddVettedApplicationToBatchService(document_number=document_number)
        service.add_to_batch()
        self.logger.info("End gazette process")
