from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from app.models import Application
from app.api.serializers import ApplicationSerializer
from app.views.filters.application_filter import ApplicationModelFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class ApplicationListView(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationModelFilter
    pagination_class = StandardResultsSetPagination
