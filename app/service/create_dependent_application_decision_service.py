import logging
from typing import List, Optional, Type


from app.models import (
    ApplicationDecision,
    DependentApplicationDecision,
    ApplicationDecisionType,
)
from app_personal_details.models import Spouse, Permit, Child
from app_production.api.dto import PermitRequestDTO


class CreateDependentApplicationDecisionService:

    def _fetch_related_objects(
        self, model: Type, document_number: str, object_type: str
    ) -> List:
        self.logger.debug(
            f"Fetching {object_type} objects for document number: {document_number}."
        )
        return list(model.objects.filter(document_number=document_number))

    def _get_child_list(self, document_number: str) -> List[Child]:
        return self._fetch_related_objects(Child, document_number, "child")

    def _get_spouse_list(self, document_number: str) -> List[Spouse]:
        return self._fetch_related_objects(Spouse, document_number, "spouse")

    def get_model_info(self, obj) -> str:
        return f"{obj._meta.app_label}.{obj._meta.model_name}"

    def create_spouse_application_decision(self, document_number: str):
        self.logger.debug(
            f"Creating application decisions for spouses with document number: {document_number}."
        )
        spouses = self._get_spouse_list(document_number)
        principal_decision = self.principal_application_decision(document_number)
        if not principal_decision:
            self.logger.warning(
                "No principal application decision found. Skipping spouse creation."
            )
            return
        for spouse in spouses:
            self._create_application_decision_if_not_exists(spouse, principal_decision)

    def create_child_application_decision(self, document_number: str):
        self.logger.debug(
            f"Creating application decisions for children with document number: {document_number}."
        )
        children = self._get_child_list(document_number)
        principal_decision = self.principal_application_decision(document_number)
        if not principal_decision:
            self.logger.warning(
                "No principal application decision found. Skipping child creation."
            )
            return
        for child in children:
            self._create_application_decision_if_not_exists(child, principal_decision)

    def _create_application_decision_if_not_exists(
        self, obj, principal_decision: ApplicationDecision
    ):
        parent_object_id = obj.id
        parent_object_type = self.get_model_info(obj)
        if not self._get_existing_dependent_application_decision_base(
            parent_object_id, parent_object_type
        ):
            self.create_new_dependent_application_decision(
                principal_decision_type=principal_decision,
                parent_object_id=parent_object_id,
                parent_object_type=parent_object_type,
                dependent_decision=principal_decision.proposed_decision_type,
            )
        else:
            self.logger.info(
                f"Application decision already exists for {parent_object_type} with ID {parent_object_id}."
            )

    def principal_application_decision(
        self, document_number: str
    ) -> Optional[ApplicationDecision]:
        self.logger.debug(
            f"Fetching principal application decision for document number: {document_number}."
        )
        try:
            return ApplicationDecision.objects.get(
                document_number=document_number,
                proposed_decision_type__code__iexact="ACCEPTED",
            )
        except ApplicationDecision.DoesNotExist:
            self.logger.warning(
                f"No principal application decision found for document number: {document_number}."
            )
            return None

    def check_application_decision(self, document_number: str) -> bool:
        self.logger.debug(
            f"Checking if application decision exists for document number: {document_number}."
        )
        return ApplicationDecision.objects.filter(
            document_number=document_number
        ).exists()

    def create_dependents_application_decision(self, document_number: str):
        self.logger.info(
            f"Creating dependent application decisions for document number: {document_number}."
        )
        if (
            self.is_allowed_create_dependent_application_decision()
            and self.check_application_decision(document_number)
        ):
            self.create_spouse_application_decision(document_number)
            self.create_child_application_decision(document_number)
        else:
            self.logger.warning(
                f"No accepted application decision or not allowed for document number: {document_number}."
            )

    def _get_existing_dependent_application_decision_base(
        self, parent_object_id: int, parent_object_type: str
    ) -> Optional[DependentApplicationDecision]:
        self.logger.debug(
            f"Checking existing dependent application for {parent_object_type} with ID {parent_object_id}."
        )
        return DependentApplicationDecision.objects.filter(
            parent_object_id=parent_object_id, parent_object_type=parent_object_type
        ).first()

    def create_new_dependent_application_decision(
        self,
        principal_decision_type: ApplicationDecision,
        parent_object_id: int,
        parent_object_type: str,
        dependent_decision: ApplicationDecisionType,
        applicant_type: str = "dependent",
    ):
        self.logger.info(
            f"Creating new dependent application decision for {parent_object_type} with ID {parent_object_id}."
        )
        DependentApplicationDecision.objects.create(
            document_number=self.document_number,
            parent_object_id=parent_object_id,
            parent_object_type=parent_object_type,
            principal_decision_type=principal_decision_type,
        )

    def is_allowed_create_dependent_application_decision(self) -> bool:
        # Implement actual logic here
        return False
