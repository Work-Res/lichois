
from app_assessment.models import AssessmentCaseNote, AssessmentCaseSummary
from app_assessment.api.dto import AssessmentNoteRequestDTO
from app_assessment.service import AssessmentNoteService

from .base_test import BaseTest


class AssessmentNoteServiceTestCase(BaseTest):

    def setUp(self):

        super().setUp()
        self.application = self.create_new_application()
        self.document_number = self.application.application.application_document.document_number

        self.summary = AssessmentCaseSummary.objects.create(
            document_number=self.document_number,
            summary='Test'
        )

        self.valid_payload = {
            'document_number': self.document_number,
            'parent_object_id': self.summary.id,
            'parent_object_type': 'app_assessment.AssessmentCaseSummary',
            'note_text': 'This is a test note.',
            'note_type': 'NOTE'
        }
        self.dto = AssessmentNoteRequestDTO(**self.valid_payload)
        self.service = AssessmentNoteService(note_request_dto=self.dto)

    def test_create_valid(self):
        self.assertIsNotNone(self.application)
        self.assertTrue(self.service.create())
        self.assertTrue(AssessmentCaseNote.objects.filter(document_number=self.document_number).exists())

    def test_get_assessment_notes_by_by_parent_type_and_parent_id(self):
        AssessmentCaseNote.objects.create(**self.valid_payload)
        notes = self.service.get_assessment_notes_by_by_parent_type_and_parent_id()
        self.assertEqual(notes.count(), 1)
        self.assertEqual(notes.first().document_number, self.document_number)

    def test_update_valid(self):
        pass
        # case_note = AssessmentCaseNote.objects.create(**self.valid_payload)
        # update_payload = {
        #     'document_number': self.document_number,
        #     'parent_object_id': self.summary.id,
        #     'parent_object_type': 'app_assessment.AssessmentCaseSummary',
        #     'note_text': 'This is an updated test note.'
        # }
        # update_dto = AssessmentNoteRequestDTO(**update_payload)
        # update_service = AssessmentNoteService(note_request_dto=update_dto)
        #
        # self.assertTrue(update_service.update())
        # updated_case_note = AssessmentCaseNote.objects.get(document_number=self.document_number)
        # self.assertEqual(updated_case_note.note, 'This is an updated test note.')

    def test_update_does_not_exist(self):
        update_payload = {
            'document_number': self.document_number,
            'parent_object_id': self.summary.id,
            'parent_object_type': 'app_assessment.AssessmentCaseSummary',
            'note_text': 'This note will not be updated.'
        }
        update_dto = AssessmentNoteRequestDTO(**update_payload)
        update_service = AssessmentNoteService(note_request_dto=update_dto)

        self.assertFalse(update_service.update())
        self.assertFalse(AssessmentCaseNote.objects.filter(document_number=self.document_number).exists())
