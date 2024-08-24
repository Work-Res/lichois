import django_filters
from gazette.models import Batch
from gazette.models.choices import BATCH_STATUS_CHOICES


class BatchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name='status', choices=BATCH_STATUS_CHOICES)
    date_of_publish = django_filters.DateFromToRangeFilter(field_name='date_of_publish')

    class Meta:
        model = Batch
        fields = ['title', 'status', 'date_of_publish']
