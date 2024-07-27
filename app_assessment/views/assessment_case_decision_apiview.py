from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_assessment.api.dto import AssessmentCaseDecisionDTOSerializer, AssessmentCaseDecisionDTO
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService
from app_assessment.validators import AssessmentCaseDecisionValidator


class AssessmentCaseDecisionAPIView(APIView):
    """
    API View for handling Assessment Case Decisions.
    """

    def post(self, request):
        """
        Handles POST requests for creating an assessment case decision.

        :param request: HTTP request object
        :param document_number: Document number for the assessment case
        :return: HTTP Response object
        """
        try:
            serializer = AssessmentCaseDecisionDTOSerializer(data=request.data)
            if not serializer.is_valid():
                return self._response_bad_request(serializer.errors)

            assessment_decision_request = AssessmentCaseDecisionDTO(**serializer.data)
            validator = AssessmentCaseDecisionValidator(assessment_case_decision=assessment_decision_request)

            if not validator.is_valid():
                return self._response_bad_request(validator.response.result())

            service = AssessmentCaseDecisionService(assessment_case_decision_dto=assessment_decision_request)
            service.create()
            return Response(service.response.result(), status=status.HTTP_200_OK)

        except Exception as e:
            return self._response_server_error(str(e))

    def _response_bad_request(self, errors):
        """
        Returns a 400 BAD REQUEST response.

        :param errors: Errors to be included in the response
        :return: HTTP Response object with status 400
        """
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def _response_server_error(self, error_message):
        """
        Returns a 500 INTERNAL SERVER ERROR response.

        :param error_message: Error message to be included in the response
        :return: HTTP Response object with status 500
        """
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
