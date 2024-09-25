from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_assessment.api.dto import AssessmentCaseDecisionDTO
from app_assessment.api.serializers.assessement_request_serializer import AssessmentRequestSerializer
from app_assessment.validators.assessment_case_decision_validator import AssessmentCaseDecisionValidator
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService


class AssessmentDecisionAPIView(APIView):

    def post(self, request):
        serializer = AssessmentRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Extract validated data and initialize the DTO
                data = serializer.validated_data
                assessment_case_decision = AssessmentCaseDecisionDTO(**data)

                # Validate the DTO
                validator = AssessmentCaseDecisionValidator(
                    assessment_case_decision=assessment_case_decision
                )
                assessment_case_decision.comment_type = "assessment_decision"
                if validator.is_valid():
                    # Pass the DTO to the service and return the response
                    service = AssessmentCaseDecisionService(
                        assessment_case_decision_dto=assessment_case_decision
                    )
                    return Response(
                        service.create_assessment(), status=status.HTTP_201_CREATED
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
            assessment_case_decision_dto = AssessmentCaseDecisionDTO(document_number=document_number)
            service = AssessmentCaseDecisionService(assessment_case_decision_dto)
            return service.retrieve_assessment()

        # Handle missing document_number in query params
        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
