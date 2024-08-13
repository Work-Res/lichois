from rest_framework import viewsets

from ...api.serializers import SummaryAssessmentSerializer
from ...models import SummaryAssessment


class SummaryAssessmentViewSet(viewsets.ModelViewSet):
    queryset = SummaryAssessment.objects.all()
    serializer_class = SummaryAssessmentSerializer
    lookup_field = "document_number"
