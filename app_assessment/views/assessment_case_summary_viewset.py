import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app_assessment.api.dto import CaseSummaryRequestDTO
from app_assessment.api.serializers import AssessmentCaseSummarySerializer
from app_assessment.models import AssessmentCaseSummary
from app_assessment.service import CaseSummaryService
from app_assessment.validators import AssessmentCaseSummaryValidator
from app_assessment.views.filters import AssessmentCaseSummaryFilter

logger = logging.getLogger(__name__)


class AssessmentCaseSummaryViewSet(viewsets.ModelViewSet):
    queryset = AssessmentCaseSummary.objects.all()
    serializer_class = AssessmentCaseSummarySerializer
    filterset_class = AssessmentCaseSummaryFilter

    def create(self, request, *args, **kwargs):
        try:
            case_summary_request_dto = CaseSummaryRequestDTO(**request.data)
            validator = AssessmentCaseSummaryValidator(
                assessment_case_summary=case_summary_request_dto
            )
            if not validator.is_valid():
                logger.warning(
                    "Validation failed for create request: %s",
                    validator.response.result(),
                )
                return Response(
                    validator.response.result(), status=status.HTTP_400_BAD_REQUEST
                )

            summary_service = CaseSummaryService(
                case_summary_request_dto=case_summary_request_dto
            )
            summary_service.create()
            if summary_service.response.status:
                logger.info("Assessment case summary created successfully.")
                return Response(
                    summary_service.response.result(), status=status.HTTP_201_CREATED
                )
            else:
                logger.warning(
                    "Failed to create assessment case summary: %s",
                    summary_service.response.result(),
                )
                return Response(
                    summary_service.response.result(),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.error(
                "Exception occurred while creating assessment case summary: %s",
                e,
                exc_info=True,
            )
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False, methods=["post"], url_path="save-summary", url_name="save_summary"
    )
    def save(self, request):
        try:
            case_summary_request_dto = CaseSummaryRequestDTO(**request.data)
            validator = AssessmentCaseSummaryValidator(
                assessment_case_summary=case_summary_request_dto
            )
            if not validator.is_valid_to_update():
                logger.warning(
                    "Validation failed for save request: %s",
                    validator.response.result(),
                )
                return Response(
                    validator.response.result(), status=status.HTTP_400_BAD_REQUEST
                )

            summary_service = CaseSummaryService(
                case_summary_request_dto=case_summary_request_dto
            )
            summary_service.update()

            if summary_service.response.status:
                logger.info("Assessment case summary updated successfully.")
                return Response(
                    summary_service.response.result(), status=status.HTTP_200_OK
                )
            else:
                logger.warning(
                    "Failed to update assessment case summary: %s",
                    summary_service.response.result(),
                )
                return Response(
                    summary_service.response.result(),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.error(
                "Exception occurred while updating assessment case summary: %s",
                e,
                exc_info=True,
            )
            return Response(
                {"detail": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
