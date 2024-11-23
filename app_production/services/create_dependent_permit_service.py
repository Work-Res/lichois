import logging
import random

from datetime import date
from typing import List, Optional

from django.db import transaction


from app.models import ApplicationDecision
from app.utils import ApplicationProcesses
from app_checklist.models import SystemParameter
from app_personal_details.models import Spouse, Permit, Child
from app_production.api.dto import PermitRequestDTO


class CreateDependentPermitService:
    def __init__(self, request: PermitRequestDTO):
        self.request = request
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def systems_parameter(self) -> Optional[SystemParameter]:
        self.logger.debug("Fetching system parameters for resident permit.")
        try:
            return SystemParameter.objects.get(
                application_type__icontains=ApplicationProcesses.RESIDENT_PERMIT.value
            )
        except SystemParameter.DoesNotExist:
            self.logger.error("SystemParameter for resident permit not found.")
            return None

    def _fetch_related_objects(self, model, document_number: str, object_type: str) -> List:
        self.logger.debug(f"Fetching {object_type} objects for document number: {document_number}.")
        try:
            return list(model.objects.filter(document_number=document_number))
        except model.DoesNotExist:
            self.logger.warning(f"No {object_type} found for document number: {document_number}.")
            return []

    def _get_child_list(self, document_number: str) -> List[Child]:
        return self._fetch_related_objects(Child, document_number, "child")

    def _get_spouse_list(self, document_number: str) -> List[Spouse]:
        return self._fetch_related_objects(Spouse, document_number, "spouse")

    def get_model_info(self, obj) -> str:
        return f"{obj._meta.app_label}.{obj._meta.model_name}"

    def create_spouse_permit(self, document_number: str):
        self.logger.debug(f"Creating permits for spouses of document number: {document_number}.")
        spouses = self._get_spouse_list(document_number)
        for spouse in spouses:
            self._create_permit_if_not_exists(spouse)

    def create_child_permit(self, document_number: str):
        self.logger.debug(f"Creating permits for children of document number: {document_number}.")
        children = self._get_child_list(document_number)
        for child in children:
            self._create_permit_if_not_exists(child)

    def _create_permit_if_not_exists(self, obj):
        parent_object_id = obj.id
        parent_object_type = self.get_model_info(obj)
        if not self._get_existing_permit_base(parent_object_id, parent_object_type):
            self.create_new_dependent_permit(
                parent_object_id=parent_object_id,
                parent_object_type=parent_object_type,
                applicant_type="dependent"
            )
        else:
            self.logger.info(f"Permit already exists for {parent_object_type} with ID {parent_object_id}.")

    def check_application_decision(self, document_number: str) -> bool:
        self.logger.debug(f"Checking application decision for document number: {document_number}.")
        try:
            return ApplicationDecision.objects.filter(
                document_number=document_number,
                proposed_decision_type__code__iexact="ACCEPTED",
            ).exists()
        except Exception as e:
            self.logger.error(f"Error checking application decision: {e}")
            return False

    def create_dependents(self, document_number: str):
        self.logger.info(f"Creating dependent permits for document number: {document_number}.")
        if self.check_application_decision(document_number) and self.is_allowed_create_dependent_permits():
            self.create_spouse_permit(document_number)
            self.create_child_permit(document_number)
        else:
            self.logger.warning(f"No accepted application decision for document number: {document_number}.")

    def _get_existing_permit_base(self, parent_object_id: int, parent_object_type: str) -> Optional[Permit]:
        self.logger.debug(f"Checking existing permit for {parent_object_type} with ID {parent_object_id}.")
        try:
            return Permit.objects.get(parent_object_id=parent_object_id, parent_object_type=parent_object_type)
        except Permit.DoesNotExist:
            return None

    @transaction.atomic
    def create_new_dependent_permit(
        self, parent_object_id: int, parent_object_type: str, applicant_type: str = "dependent"
    ):
        self.logger.info(f"Creating new permit for {parent_object_type} with ID {parent_object_id}.")
        try:
            security_code = self.generate_security_number()
            system_param = self.systems_parameter()
            if not system_param:
                self.logger.error("Cannot create permit: SystemParameter not found.")
                return

            Permit.objects.create(
                document_number=self.request.document_number,
                permit_type=self.request.permit_type,
                permit_no=self.request.permit_no,
                date_issued=self.request.date_issued or date.today(),
                date_expiry=system_param.valid_to,
                place_issue=self.request.place_issue,
                security_number=security_code,
                applicant_type=applicant_type,
                parent_object_id=parent_object_id,
                parent_object_type=parent_object_type,
            )
            self.logger.info(f"Permit successfully created for document number: {self.request.document_number}.")
        except Exception as e:
            self.logger.error(f"Error creating permit: {e}")

    def is_allowed_create_dependent_permits(self):
        return False

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
