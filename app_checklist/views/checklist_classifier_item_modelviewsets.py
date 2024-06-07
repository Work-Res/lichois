import django_filters

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from app_checklist.models import ChecklistClassifierItem
from ..api.serializers import ClassifierItemSerializer, ChecklistClassifierItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    max_page_size = 120


    # code = models.CharField(max_length=50)
    # name = models.CharField(max_length=100)
    # application_type = models.CharField(max_length=100)
    # description = models.TextField()
    # mandatory = models.BooleanField(default=False)
    # checklist_classifier = models.ForeignKey(ChecklistClassifier, on_delete=models.CASCADE)
    # sequence = models.IntegerField(blank=True, null=True)
    # valid_from = models.DateField()
    # valid_to = models.DateField()
    #
class ChecklistClassifierItemFilter(django_filters.FilterSet):

    classifier_code = django_filters.CharFilter(field_name='checklist_classifier__code', lookup_expr='iexact')
    process_name = django_filters.CharFilter(field_name='checklist_classifier__process_name', lookup_expr='icontains')
    mandatory = django_filters.BooleanFilter(field_name='mandatory')
    application_type = django_filters.CharFilter(field_name='application_type', lookup_expr='iexact')
    valid_from = django_filters.DateFilter(field_name='valid_from', lookup_expr='gte')
    valid_to = django_filters.DateFilter(field_name='valid_to', lookup_expr='lte')

    class Meta:
        model = ChecklistClassifierItem
        exclude = ('description')


class ChecklistClassifierItemModelViewSets(viewsets.ModelViewSet):
    queryset = ChecklistClassifierItem.objects.all()
    serializer_class = ChecklistClassifierItemSerializer
    filterset_class = ChecklistClassifierItemFilter
    pagination_class = StandardResultsSetPagination
