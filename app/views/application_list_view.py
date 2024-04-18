import django_filters

from rest_framework import viewsets

from app.models import Application
from app.api.serializers import ApplicationSerializer


class ApplicationModelFilter(django_filters.FilterSet):

    application_document_number = django_filters.CharFilter(
        field_name='application__application_document__document_number', lookup_expr='icontains')
    application_status = django_filters.CharFilter(
        field_name='application__application_status', lookup_expr='icontains')
    min_created_date = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    max_created_date = django_filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Application


class ApplicationListView(viewsets.ModelViewSet):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationModelFilter

    # filterset_fields = ['application_document__document_number', 'in_stock']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     created_date = self.request.query_params.get('created_date', None)
    #     pagination_class = pagination.PageNumberPagination
    #     page_size = 10
    #
    #     if created_date:
    #         created_date = datetime.strptime(created_date, "%Y-%m-%d")
    #         queryset = Application.objects.filter(created__date=created_date)
    #     return queryset
