from rest_framework.decorators import action

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from citizenship.api.dto.citizenship_minister_decision_request_dto import CitizenshipMinisterDecisionSerializer
from citizenship.models import CitizenshipMinisterDecision
from citizenship.views.filters import CitizenshipMinisterDecisionFilter


class CitizenshipMinisterDecisionViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipMinisterDecision.objects.all()
    serializer_class = CitizenshipMinisterDecisionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CitizenshipMinisterDecisionFilter

    @action(detail=False, methods=['get'], url_path='search-by-document-number/(?P<document_number>[^/.]+)')
    def search_by_document_number(self, request, document_number=None):
        """
        Custom GET method to search CitizenshipMinisterDecision by document_number
        """
        try:
            decision = CitizenshipMinisterDecision.objects.get(document_number=document_number)
            serializer = self.get_serializer(decision)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CitizenshipMinisterDecision.DoesNotExist:
            return Response({'error': 'Citizenship Minister Decision not found'}, status=status.HTTP_404_NOT_FOUND)
