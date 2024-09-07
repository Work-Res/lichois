from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_assessment.api.dto import (
    AssessmentNoteRequestDTOSerializer,
    AssessmentNoteRequestDTO, )

from app_assessment.service import AssessmentNoteService
from app_assessment.validators.assessment_note_validator import AssessmentNoteValidator


class ReviewDecisionAPIView(APIView):

    def post(self, request):
        serializer = AssessmentNoteRequestDTOSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Extract validated data and initialize the DTO
                data = serializer.validated_data
                assessment_note_request = AssessmentNoteRequestDTO(**data)

                # Validate the DTO
                validator = AssessmentNoteValidator(
                    assessment_note_request_dto=assessment_note_request
                )
                if validator.is_valid():
                    # Pass the DTO to the service and return the response
                    service = AssessmentNoteService(
                        note_request_dto=assessment_note_request
                    )
                    return Response(
                        service.create_review(), status=status.HTTP_201_CREATED
                    )
                else:
                    # Return validation errors if the validator fails
                    return Response(
                        {"detail": "Validation failed", "errors": validator.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Return serializer errors if the data is invalid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            # Handle unexpected exceptions
            return JsonResponse(
                {"error": f"An error occurred while processing the request: {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        document_number = request.query_params.get("document_number")
        if document_number:
            # Create DTO and pass to service for retrieval
            assessment_note_dto = AssessmentNoteRequestDTOSerializer(document_number=document_number)
            service = AssessmentNoteService(note_request_dto=assessment_note_dto)
            return service.retrieve_review()

        # Handle missing document_number in query params
        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
