import logging

from django.db import transaction, IntegrityError


from app_assessment.api.dto import CaseSummaryRequestDTO
from app_assessment.api.serializers import AssessmentCaseSummarySerializer
from app_assessment.models import AssessmentCaseSummary

from app.api.common.web import APIResponse, APIMessage


class CaseSummaryService:

    def __init__(self, case_summary_request_dto: CaseSummaryRequestDTO):
        self.case_summary_request_dto = case_summary_request_dto
        self.response = APIResponse()

    def update(self):
        self.logger.info(
            f"Updating a case note for {self.case_summary_request_dto.document_number}"
        )
        try:
            with transaction.atomic():
                # Fetch the existing case note
                case_note = AssessmentCaseSummary.objects.get(
                    document_number=self.case_summary_request_dto.document_number,
                    parent_object_id=self.case_summary_request_dto.parent_object_id,
                    parent_object_type=self.case_summary_request_dto.parent_object_type,
                )
                self.logger.debug(
                    f"Fetched assessement case summary for {self.case_summary_request_dto.document_number}"
                )

                updated_data = self.case_summary_request_dto.__dict__
                for key, value in updated_data.items():
                    setattr(case_note, key, value)
                case_note.save()
                self.logger.info(f"Updated assessement case summary for {self.case_summary_request_dto.document_number}")
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been updated.",
                    details=f"Assessment note has been updated for {self.case_summary_request_dto.document_number}"
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except AssessmentCaseSummary.DoesNotExist:
            self.logger.error(
                f"Case note with document number  {self.case_summary_request_dto.document_number} does not exist."
            )
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")

    def create(self):
        self.logger.info(
            f"Creating a assessment case summary for {self.case_summary_request_dto.document_number}"
        )
        try:
            with transaction.atomic():
                assessment_case_summary = AssessmentCaseSummary.objects.create(
                    **self.case_summary_request_dto
                )
                api_message = APIMessage(
                    code=200,
                    message="Assessment summary has been created.",
                    details="Assessment summary has been created.",
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
                self.response.data = AssessmentCaseSummarySerializer(
                    data=assessment_case_summary
                ).data
                self.logger.info(
                    f"Created assessment summary created for {self.case_summary_request_dto.document_number}"
                )
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")
            self.response.status = False
            api_message = APIMessage(
                code=400,
                message="Failed to create assessment summary.",
                details=f"Failed to create assessment summary for {self.case_summary_request_dto.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
