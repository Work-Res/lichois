from rest_framework import viewsets

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewSerializer
from citizenship.models import Interview
from citizenship.views.board.filter import InterviewFilter


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    filterset_class = InterviewFilter
    pagination_class = StandardResultsSetPagination
