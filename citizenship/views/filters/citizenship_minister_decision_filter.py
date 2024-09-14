import django_filters

from citizenship.models import CitizenshipMinisterDecision


class CitizenshipMinisterDecisionFilter(django_filters.FilterSet):
    date_requested = django_filters.DateFromToRangeFilter()  # filter between date ranges
    date_approved = django_filters.DateFromToRangeFilter()  # filter between date ranges
    document_number = django_filters.CharFilter(lookup_expr='icontains')  # filter by partial match  # filter by status

    class Meta:
        model = CitizenshipMinisterDecision
        fields = ['document_number', 'date_requested', 'date_approved']
