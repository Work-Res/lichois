import logging
import random
from datetime import date, datetime

from django.db import transaction

from app.api.common.web import APIMessage, APIResponse
from app.models import Application, ApplicationDecision
from app_checklist.models import SystemParameter
from app_personal_details.models import Permit
from workresidentpermit.classes.service.word import WorkAndResidentLetterContextGenerator, \
    WorkAndResidentLetterProductionProcess

from ..api.dto import PermitRequestDTO
from ..handlers.postsave.upload_document_production_handler import UploadDocumentProductionHandler


class PermitProductionService:
    """Responsible for creating a new permit when production is accepted."""

    def __init__(self, request: PermitRequestDTO):
        self.request = request
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._systems_parameter = None
        self.response = APIResponse()

    def systems_parameter(self):
        try:
            print("self.request.application_type ", self.request.application_type)
            self._systems_parameter = SystemParameter.objects.get(
                application_type__icontains=self.request.application_type
            )
        except SystemParameter.DoesNotExist:
            pass
        return self._systems_parameter

    def _get_existing_permit(self, applicant_type='applicant'):
        try:
            permit = Permit.objects.get(document_number=self.request.document_number,
                                        applicant_type=applicant_type)
        except Permit.DoesNotExist:
            pass
        else:
            return permit

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

    def generate_permint_number(self):
        return self.request.permit_no

    @transaction.atomic
    def create_new_permit(self, applicant_type='applicant'):
        permit = self._get_existing_permit()
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

    def invalidate_existing_permit(self):
        pass

    def parse_iso_date(self, date_input):
        if not isinstance(date_input, str):
            raise ValueError("fromisoformat: argument must be str")
        return datetime.fromisoformat(date_input)

    def get_context_data(self):
        pass

    def allowed_to_generate_document(self):
        return False

    def _get_application(self):
        try:
            return Application.objects.get(
                application_document__document_number=self.request.document_number
            )
        except Application.DoesNotExist:
            pass

    def _get_application_decision(self):
        try:
            return ApplicationDecision.objects.get(
                document_number=self.request.document_number
            )
        except ApplicationDecision.DoesNotExist:
            pass

    def create_document(self):
        if self.allowed_to_generate_document():
            application = self._get_application()
            decision = self._get_application_decision()
            handler = UploadDocumentProductionHandler()
            context_generator = WorkAndResidentLetterContextGenerator()
            process = WorkAndResidentLetterProductionProcess(handler, context_generator)
            process.handle(application=application, decision=decision, document_number=self.request.document_number)
        else:
            print("Not configured to generate document")
