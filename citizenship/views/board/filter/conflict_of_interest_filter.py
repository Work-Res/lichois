import django_filters

from citizenship.models import ConflictOfInterest


class ConflictOfInterestFilter(django_filters.FilterSet):
    attendee = django_filters.UUIDFilter(field_name='attendee__id', lookup_expr='exact')
    application = django_filters.UUIDFilter(field_name='application__id', lookup_expr='exact')
    document_number = django_filters.CharFilter(field_name='application__application_document__document_number', lookup_expr='exact')
    has_conflict = django_filters.BooleanFilter(field_name='has_conflict')
    declared_at = django_filters.DateTimeFilter(field_name='declared_at', lookup_expr='exact')
    declared_before = django_filters.DateTimeFilter(field_name='declared_at', lookup_expr='lte')
    declared_after = django_filters.DateTimeFilter(field_name='declared_at', lookup_expr='gte')

    class Meta:
        model = ConflictOfInterest
        fields = ['attendee', 'application', 'document_number', 'has_conflict', 'declared_at']
