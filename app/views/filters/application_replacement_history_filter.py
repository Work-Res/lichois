import django_filters


from rest_framework.pagination import PageNumberPagination

from app.models import ApplicationReplacementHistory


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class ApplicationReplacementHistoryFilter(django_filters.FilterSet):

    application_type = django_filters.CharFilter(
        field_name='application_type', lookup_expr='icontains')

    user_identifier = django_filters.BooleanFilter(field_name='application_user__user_identifier')

    process_name = django_filters.CharFilter(
        field_name='process_name', lookup_expr='icontains')

    class Meta:
        model = ApplicationReplacementHistory
        exclude = ('historical_record',)
