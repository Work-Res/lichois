from rest_framework import viewsets

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse


class InterviewResponseViewSet(viewsets.ModelViewSet):
    queryset = InterviewResponse.objects.all()
    serializer_class = InterviewResponseSerializer
    pagination_class = StandardResultsSetPagination
