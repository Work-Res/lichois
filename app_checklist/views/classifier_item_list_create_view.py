import django_filters

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from app_checklist.models import ClassifierItem
from ..api.serializers import  ClassifierItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    max_page_size = 120


class ClassifierItemFilter(django_filters.FilterSet):

    classifier_code = django_filters.CharFilter(field_name='classifier__code', lookup_expr='iexact')
    process = django_filters.CharFilter(field_name='classifier__code', lookup_expr='icontains')
    valid_from = django_filters.DateFilter(field_name='valid_from', lookup_expr='gte')
    valid_to = django_filters.DateFilter(field_name='valid_to', lookup_expr='lte')

    class Meta:
        model = ClassifierItem
        exclude = ('sequence')


class ClassifierItemListCreateView(viewsets.ModelViewSet):
    queryset = ClassifierItem.objects.all()
    serializer_class = ClassifierItemSerializer
    filterset_class = ClassifierItemFilter
    pagination_class = StandardResultsSetPagination
