import django_filters

from citizenship.models import Interview


class InterviewFilter(django_filters.FilterSet):
    scheduled_time = django_filters.DateTimeFilter(field_name='scheduled_time', lookup_expr='exact')
    scheduled_time_before = django_filters.DateTimeFilter(field_name='scheduled_time', lookup_expr='lte')
    scheduled_time_after = django_filters.DateTimeFilter(field_name='scheduled_time', lookup_expr='gte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    variation_type = django_filters.CharFilter(field_name='variation_type', lookup_expr='exact')
    conducted = django_filters.BooleanFilter(field_name='conducted')

    class Meta:
        model = Interview
        fields = ['scheduled_time', 'status', 'variation_type']
