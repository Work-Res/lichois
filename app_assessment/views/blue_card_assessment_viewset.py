from rest_framework import viewsets
from ..models import BlueCardAssessment
from ..api.serializers import BlueCardAssessmentSerializer


class BlueCardAssessmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing BlueCardAssessment instances.
    """

    queryset = BlueCardAssessment.objects.all()
    serializer_class = BlueCardAssessmentSerializer
    lookup_field = "document_number"
