from datetime import date
import json
import logging
from django.shortcuts import get_object_or_404

from app_checklist.models import SystemParameter
from workresidentpermit.classes import historical_record
from workresidentpermit.exceptions import WorkResidentPermitApplicationDecisionException

from app.models import (
    ApplicationDecisionType,
    ApplicationDecision,
    ApplicationStatus,
    Application,
    ApplicationAppealHistory,
)

from app.utils.system_enums import ApplicationProcesses
from app_production.services.permit_production_service import PermitProductionService

from ..api.dto.permit_request_dto import PermitRequestDTO


class AppealProductionService(PermitProductionService):

    process_name = ApplicationProcesses.WORK_RESIDENT_PERMIT.value

    def __init__(self, request: PermitRequestDTO):
        self.request = request
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._systems_parameter = None
        self.appeal_document_number = request.document_number
        self.request.document_number = self._get_document_number()
        super().__init__(request=self.request)

    def create_new_permit(self):
        try:
            decision = ApplicationDecision.objects.get(
                document_number=self.request.document_number,
            )
        except ApplicationDecision.DoesNotExist:
            self.logger.error(
                f"Application decision for document number {self.request.document_number} does not exist."
            )
        else:
            decision.proposed_decision_type = self.proposed_application_decision_type()
            decision.save()
            super().create_new_permit()

    def proposed_application_decision_type(self):
        try:
            proposed_application_decision_type = get_object_or_404(
                ApplicationDecisionType, code__iexact="ACCEPTED"
            )
            return proposed_application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            error_message = f"Application decision type cannot be found using decision_type: {self.decision_value}"
            self.logger.error(error_message)
            raise WorkResidentPermitApplicationDecisionException(error_message)

    def _get_application_status(self):
        return ApplicationStatus.objects.get(name="ACCEPTED")

    def systems_parameter(self):

        application = self._get_application()
        application.application_status = self._get_application_status()
        application.save()
        self.request.permit_type = application.application_type
        self.request.application_type = application.application_type
        self.request.place_issue = "Gaborone"
        print(
            f"---------------Document number for system param: {self.request.document_number}--------"
        )
        try:
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=application.application_type,
                document_number=self.request.document_number,
            )
            self.logger.info(
                f"System parameter found for {self.request.application_type}, returning existing one."
            )
        except SystemParameter.DoesNotExist:
            self.logger.info(
                f"System parameter not found for {self.request.application_type}, creating a new one."
            )
            self._systems_parameter = SystemParameter.objects.create(
                application_type=application.application_type,
                valid_from=date.today(),
                valid_to=date.today(),
                duration_type="years",
                duration=5,
                document_number=self.request.document_number,
            )
        return self._systems_parameter

    def _get_history_application(self):
        print(
            f"Appeal document number *************{self.appeal_document_number}********"
        )
        try:
            app = Application.objects.get(
                application_document__document_number=self.appeal_document_number
            )
        except Application.DoesNotExist:
            self.logger.error(
                f"Application with document number {self.appeal_document_number} does not exist."
            )
        else:
            application_type = app.application_type
            process_name = application_type.split("_APPEAL")[0]
            applicant = app.application_document.applicant
            history = ApplicationAppealHistory.objects.filter(
                application_user=applicant,
                process_name=process_name,
            ).first()
            return history
        return None

    def _get_document_number(self):
        try:
            # Extract the document number from the historical record
            his_record = self._get_history_application()
            data = his_record.historical_record.get("data", [])
            if data:
                document_number = data[0].get("document_number")
                return document_number
            return None
        except (KeyError, IndexError, TypeError) as e:
            print(f"An error occurred while extracting document number: {e}")
            return None
