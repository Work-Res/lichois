from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from app_assessment.api.dto import AssessmentCaseDecisionDTO
from app_assessment.api.serializers import AssessmentCaseDecisionSerializer
from app_assessment.models import AssessmentCaseDecision
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService
from app_assessment.validators import AssessmentCaseDecisionValidator
from app_assessment.views.filters import AssessmentCaseDecisionFilter


class AssessmentCaseDecisionViewSet(viewsets.ModelViewSet):

    queryset = AssessmentCaseDecision.objects.all()
    serializer_class = AssessmentCaseDecisionSerializer
    filterset_class = AssessmentCaseDecisionFilter

    @action(detail=False, methods=['post'], url_path='save-decision', url_name='save_decision')
    def save(self, request):
        case_decision_request_dto = AssessmentCaseDecisionDTO(**request.data)
        validator = AssessmentCaseDecisionValidator(assessment_case_decision=case_decision_request_dto)
        # Perform your custom validation logic
        if not validator.is_valid_for_update():
            return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)
        service = AssessmentCaseDecisionService(case_decision_request_dto=case_decision_request_dto)
        service.update()
        return Response(service.response.result(), status=status.HTTP_201_CREATED)
