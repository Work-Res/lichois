from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from app_assessment.api.dto import CaseSummaryRequestDTO
from app_assessment.api.serializers import AssessmentCaseSummarySerializer
from app_assessment.models import AssessmentCaseSummary
from app_assessment.service import CaseSummaryService
from app_assessment.validators import AssessmentCaseSummaryValidator


class AssessmentCaseSummaryViewSet(viewsets.ModelViewSet):

    queryset = AssessmentCaseSummary.objects.all()
    serializer_class = AssessmentCaseSummarySerializer

    def create(self, request, *args, **kwargs):
        case_summary_request_dto = CaseSummaryRequestDTO(**request.data)
        validator = AssessmentCaseSummaryValidator(assessment_case_summary=case_summary_request_dto)
        if not validator.is_valid():
            return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)

        summary_service = CaseSummaryService(case_summary_request_dto=case_summary_request_dto)
        summary_service.create()
        if summary_service.response.status:
            return Response(summary_service.response.result(), status=status.HTTP_201_CREATED)
        else:
            return Response(summary_service.response.result(), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='save-summary', url_name='save_summary')
    def save(self, request):
        case_summary_request_dto = CaseSummaryRequestDTO(**request.data)
        validator = AssessmentCaseSummaryValidator(assessment_case_summary=case_summary_request_dto)
        if not validator.is_valid_to_update():
            return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)
        summary_service = CaseSummaryService(case_summary_request_dto=case_summary_request_dto)
        summary_service.update()

        return Response(summary_service.response.result(), status=status.HTTP_201_CREATED)
