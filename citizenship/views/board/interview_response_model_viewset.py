from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse
from citizenship.views.board.filter import InterviewResponseFilter


class InterviewResponseViewSet(viewsets.ModelViewSet):
    queryset = InterviewResponse.objects.all()
    serializer_class = InterviewResponseSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = InterviewResponseFilter
