import logging

from django.db import transaction, IntegrityError

from app.api.common.web import APIResponse, APIMessage
from ..api.dto import AssessmentNoteRequestDTO
from ..models import AssessmentCaseNote


class AssessmentNoteService:

    logger = logging.getLogger(__name__)

    def __init__(self, note_request_dto: AssessmentNoteRequestDTO):
        self.note_request_dto = note_request_dto
        self.response = APIResponse()

    def create(self):
        self.logger.info(
            f"Creating a case note for {self.note_request_dto.document_number}"
        )
        try:
            with transaction.atomic():
                AssessmentCaseNote.objects.create(**self.note_request_dto)
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been created.",
                    details="Assessment note has been created.",
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
                self.logger.info(
                    f"Created a case note for {self.note_request_dto.document_number}"
                )
                return True
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")

    def get_assessment_notes_by_by_parent_type_and_parent_id(self):
        return AssessmentCaseNote.objects.filter(
            parent_object_id=self.note_request_dto.parent_object_id,
            parent_object_type=self.note_request_dto.parent_object_type,
            document_number=self.note_request_dto.document_number,
        )

    def update(self):
        self.logger.info(
            f"Updating a case note for {self.note_request_dto.document_number}"
        )
        try:
            with transaction.atomic():
                # Fetch the existing case note
                case_note = AssessmentCaseNote.objects.get(
                    document_number=self.note_request_dto.document_number,
                    parent_object_id=self.note_request_dto.parent_object_id,
                    parent_object_type=self.note_request_dto.parent_object_type,
                )
                self.logger.debug(
                    f"Fetched case note for {self.note_request_dto.document_number}"
                )

                updated_data = self.note_request_dto.__dict__
                for key, value in updated_data.items():
                    setattr(case_note, key, value)
                case_note.save()
                self.logger.info(
                    f"Updated case note for {self.note_request_dto.document_number}"
                )
                api_message = APIMessage(
                    code=200,
                    message="Assessment note has been updated.",
                    details="Assessment note has been updated.",
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except AssessmentCaseNote.DoesNotExist:
            self.logger.error(
                f"Case note with document number  {self.note_request_dto.document_number} does not exist."
            )
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")
