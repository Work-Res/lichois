import django_filters

from citizenship.models import MeetingSession


class MeetingSessionFilter(django_filters.FilterSet):
    meeting = django_filters.CharFilter(field_name='meeting__id', lookup_expr='exact')
    title = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    start_time = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')
    batch_application_complete = django_filters.BooleanFilter()

    class Meta:
        model = MeetingSession
        fields = ['meeting', 'title', 'date', 'start_time', 'end_time', 'batch_application_complete']
