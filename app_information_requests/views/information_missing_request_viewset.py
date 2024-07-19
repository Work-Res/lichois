from rest_framework import filters

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination

from app_information_requests.api.serializers.serializer import InformationMissingRequestSerializer
from app_information_requests.models.missing_details import InformationMissingRequest
from app_information_requests.views.filters import InformationMissingRequestFilter


class InformationMissingRequestViewSet(viewsets.ModelViewSet):
    queryset = InformationMissingRequest.objects.all()
    serializer_class = InformationMissingRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = InformationMissingRequestFilter
    pagination_class = StandardResultsSetPagination
