import django_filters
from gazette.models import BatchApplication


class BatchApplicationFilter(django_filters.FilterSet):
    batch = django_filters.CharFilter(field_name='batch__name', lookup_expr='icontains')
    application = django_filters.CharFilter(field_name='application__applicant_name', lookup_expr='icontains')
    included_in_final_list = django_filters.BooleanFilter()
    reviewed_by_legal = django_filters.BooleanFilter()
    reviewed_by_ag = django_filters.BooleanFilter()

    class Meta:
        model = BatchApplication
        fields = ['batch', 'application', 'included_in_final_list', 'reviewed_by_legal', 'reviewed_by_ag']