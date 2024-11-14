import django_filters
from app.models import ApplicationRenewalHistory, ApplicationDocument


class ApplicationRenewalHistoryFilter(django_filters.FilterSet):
    application_type = django_filters.CharFilter(
        field_name='application_type', lookup_expr='icontains'
    )
    user_identifier = django_filters.BooleanFilter(
        field_name='application_user__user_identifier'
    )
    process_name = django_filters.CharFilter(
        field_name='process_name', lookup_expr='icontains'
    )
    document_number = django_filters.CharFilter(
        field_name='application_user__applicationdocument__document_number',
        lookup_expr='icontains'
    )

    class Meta:
        model = ApplicationRenewalHistory
        exclude = ('historical_record',)
