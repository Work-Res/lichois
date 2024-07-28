from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..api.dto import AssessmentNoteRequestDTO, AssessmentNoteRequestDTOSerializer
from ..service import AssessmentNoteService
from ..validators.assessment_note_validator import AssessmentNoteValidator


class AssessmentNoteViewSet(viewsets.ViewSet):
    """
    A ViewSet for creating, updating, and retrieving assessment notes.
    """

    def create(self, request):
        serializer = AssessmentNoteRequestDTOSerializer(data=request.data)
        if serializer.is_valid():
            note_request_dto = AssessmentNoteRequestDTO(**serializer.validated_data)
            validator = AssessmentNoteValidator(assessment_note_request_dto=note_request_dto)

            if not validator.is_valid():
                return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)

            service = AssessmentNoteService(note_request_dto)
            if service.create():
                return Response(service.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(service.response.result(), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='notes', name='get-notes')
    def get_notes(self, request):
        serializer = AssessmentNoteRequestDTOSerializer(data=request.query_params)
        note_request_dto = AssessmentNoteRequestDTO(**serializer.validated_data)
        service = AssessmentNoteService(note_request_dto)
        notes = service.get_assessment_notes_by_by_parent_type_and_parent_id()
        notes_data = [note for note in notes.values()]
        return Response(notes_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        serializer = AssessmentNoteRequestDTOSerializer(data=request.data)
        if serializer.is_valid():
            note_request_dto = AssessmentNoteRequestDTO(**serializer.validated_data)
            validator = AssessmentNoteValidator(assessment_note_request_dto=note_request_dto)

            if not validator.is_valid_to_update():
                return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)

            service = AssessmentNoteService(note_request_dto)
            if service.update():
                return Response(service.response.result(), status=status.HTTP_200_OK)
            else:
                return Response(service.response.result(), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
