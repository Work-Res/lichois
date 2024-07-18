from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..api.serializers import DependantAssessmentSerializer
from ..models import DependantAssessment


class DependantAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DependantAssessment.objects.all()
    serializer_class = DependantAssessmentSerializer

    action(
        detail=False,
        methods=["get"],
        url_path="dependants-assessment/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="dependants-assessment",
    )

    def check_dependant_assessment(self, request, document_number):
        # Get all the dependant assessments for a document number
        dependant_assessments = DependantAssessment.objects.filter(
            document_number=document_number
        )
        # Serialize the queryset with many=True to handle multiple objects
        serializer = DependantAssessmentSerializer(dependant_assessments, many=True)
        # Return the serialized dependant assessments
        return Response(data=serializer.data)
