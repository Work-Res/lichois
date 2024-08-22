import django_filters

from citizenship.models import Meeting
from citizenship.models.board.choices import STATUS_CHOICES


class MeetingFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    time = django_filters.TimeFilter(field_name='time', lookup_expr='exact')
    location = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name='status', choices=STATUS_CHOICES)
    start_date = django_filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='end_date', lookup_expr='lte')
    board = django_filters.CharFilter(field_name='board__id', lookup_expr='exact')

    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time', 'location', 'status', 'start_date', 'end_date', 'board']
