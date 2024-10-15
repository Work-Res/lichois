import django_filters
from citizenship.models import Section10bApplicationDecisions


class Section10bApplicationDecisionsFilter(django_filters.FilterSet):
    """Filter for Section10bApplicationDecisions."""
    mlha_director_decision = django_filters.CharFilter(lookup_expr='icontains')
    deputy_permanent_secretary = django_filters.CharFilter(lookup_expr='icontains')
    permanent_secretary = django_filters.CharFilter(lookup_expr='icontains')
    pres_permanent_secretary = django_filters.CharFilter(lookup_expr='icontains')
    president_decision = django_filters.CharFilter(lookup_expr='icontains')

    document_number = django_filters.CharFilter(
        field_name='application__application_document__document_number', lookup_expr='icontains')
    application_type = django_filters.CharFilter(field_name='application__application_type')
    application_status = django_filters.CharFilter(field_name='application__application_status__code')

    class Meta:
        model = Section10bApplicationDecisions
        fields = [
            'mlha_director_decision',
            'deputy_permanent_secretary',
            'permanent_secretary',
            'pres_permanent_secretary',
            'president_decision',
        ]
