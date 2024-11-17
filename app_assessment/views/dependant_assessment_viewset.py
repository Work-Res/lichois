from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app_personal_details.models import Spouse, Child
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
        methods=["post"],
        url_path="create-spouse",
        url_name="create_spouse",
    )
    def create_spouse_dependant_assessment(self, request):
        """Custom API to create a DependantAssessment for a Spouse"""
        spouse_id = request.data.get("spouse_id")
        if not spouse_id:
            return Response(
                {"error": "spouse_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            spouse = Spouse.objects.get(id=spouse_id)
        except Spouse.DoesNotExist:
            return Response(
                {"error": f"Spouse with id {spouse_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data["spouse"] = spouse.id  # Associate the spouse

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_path="create-child",
        url_name="create_child",
    )
    def create_child_dependant_assessment(self, request):
        """Custom API to create a DependantAssessment for a Child"""
        child_id = request.data.get("child_id")
        if not child_id:
            return Response(
                {"error": "child_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return Response(
                {"error": f"Child with id {child_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data["child"] = child.id  # Associate the child

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        url_path="is-done/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="is_done",
    )
    def is_assessment_done(self, request, document_number):
        """
        Check if all associated Spouses and Children have a DependantAssessment record.
        Return false if any does not, otherwise true.
        """
        # Get all spouses and children associated with the document_number
        spouses = Spouse.objects.filter(document_number=document_number)
        children = Child.objects.filter(document_number=document_number)

        # Check if any Spouse does not have a DependantAssessment
        for spouse in spouses:
            if not DependantAssessment.objects.filter(spouse=spouse).exists():
                return Response(
                    data={
                        "is_done": False,
                        "missing_spouse": spouse.id,
                    },
                    status=status.HTTP_200_OK,
                )

        # Check if any Child does not have a DependantAssessment
        for child in children:
            if not DependantAssessment.objects.filter(child=child).exists():
                return Response(
                    data={
                        "is_done": False,
                        "missing_child": child.id,
                    },
                    status=status.HTTP_200_OK,
                )

        # If all Spouses and Children have assessments
        return Response(data={"is_done": True}, status=status.HTTP_200_OK)
