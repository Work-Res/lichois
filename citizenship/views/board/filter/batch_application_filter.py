import django_filters

from citizenship.models import BatchApplication


class BatchApplicationFilter(django_filters.FilterSet):
    batch = django_filters.UUIDFilter(field_name='batch__id', lookup_expr='exact')
    application = django_filters.UUIDFilter(field_name='application__id', lookup_expr='exact')
    meeting_session = django_filters.UUIDFilter(field_name='meeting_session__id', lookup_expr='exact')
    meeting = django_filters.UUIDFilter(field_name='meeting_session__meeting__id', lookup_expr='exact')

    class Meta:
        model = BatchApplication
        fields = ['batch', 'application', 'meeting_session', 'meeting']
