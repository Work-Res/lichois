from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response

from ..api.serializers import DependantAssessmentSerializer
from ..models.dependant_assessment import DependantAssessment


class DependantAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DependantAssessment.objects.all()
    serializer_class = DependantAssessmentSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="all/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="all",
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

    @action(
        detail=False,
        methods=["get"],
        url_path="is-done/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="is_done",
    )
    def is_assessment_done(self, request, document_number):

        if not DependantAssessment.objects.filter(document_number=document_number).exists():
            return Response(data={"is_done": True}, status=status.HTTP_200_OK)
        # Check if any DependantAssessment has assessment == "Pending" for the given document number
        if DependantAssessment.objects.filter(
                document_number=document_number, assessment="Pending"
        ).exists():
            # Return False if a "Pending" assessment exists
            return Response(data={"is_done": False}, status=status.HTTP_200_OK)

        # Check if any DependantAssessment has assessment == "Done" for the given document number
        is_done = DependantAssessment.objects.filter(
            document_number=document_number, assessment="Done"
        ).exists()

        # Return True if an assessment with "Done" exists and no "Pending" assessment was found
        return Response(data={"is_done": is_done}, status=status.HTTP_200_OK)
