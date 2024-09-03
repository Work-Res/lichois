from django_filters import rest_framework as filters
from citizenship.models import ConflictOfInterestDuration


class ConflictOfInterestDurationFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='end_time', lookup_expr='lte')
    status = filters.ChoiceFilter(choices=ConflictOfInterestDuration.STATUS_CHOICES)
    meeting_session = filters.CharFilter(field_name='meeting_session__id')
    meeting = filters.CharFilter(field_name='meeting_session__meeting__id')

    class Meta:
        model = ConflictOfInterestDuration
        fields = ['start_time', 'end_time', 'status', 'meeting_session', 'meeting']
