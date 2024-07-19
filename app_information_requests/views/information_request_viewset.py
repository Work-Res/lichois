from rest_framework import viewsets
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from app_information_requests.api.serializers.serializer import InformationRequestSerializer
from app_information_requests.models import InformationRequest
from app_information_requests.views.filters import InformationRequestFilter


class InformationRequestViewSet(viewsets.ModelViewSet):
    queryset = InformationRequest.objects.all()
    serializer_class = InformationRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = InformationRequestFilter
    pagination_class = StandardResultsSetPagination
