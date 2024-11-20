from django.db import transaction

from datetime import date, datetime

from app.api.common.web import APIMessage
from app_personal_details.models import Spouse, Permit


class CreateDependentPermitService:

    def create_spouse_permit(self, document_number):
        try:
            spouses = Spouse.objects.get(
                document_number=document_number
            )
        except Spouse.DoesNotExists:
            pass

    def create_child_permit(self, document_number):
        pass

    def check_application_decision(self):
        pass

    def create_dependents(self):
        pass


    @transaction.atomic
    def create_new_permit(self, applicant_type='dependent'):
        permit = self._get_existing_permit(applicant_type=applicant_type)
        date_expiry = self.systems_parameter().valid_to
        if not permit:
            security_code = self.generate_security_number()
            Permit.objects.create(
                document_number=self.request.document_number,
                permit_type=self.request.permit_type,
                permit_no=self.request.permit_no,
                date_issued=self.request.date_issued or date.today(),
                date_expiry=date_expiry,
                place_issue=self.request.place_issue,
                security_number=security_code,
                applicant_type=applicant_type

            )
            print(f"Permit created successfully for {self.request.document_number}")

            api_message = APIMessage(
                code=200,
                message="Permit created successfully.",
                details="Permit created successfully.",
            )
            self.response.status = "success"
            self.response.messages.append(api_message.to_dict())
            self.logger.info(
                f"Permit created successfully for {self.request.document_number}"
            )

            try:
                self.create_document()
            except Exception as e:
                print(f"An error occurred. {e}")
            finally:
                return permit