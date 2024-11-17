import django_filters


from rest_framework.pagination import PageNumberPagination

from app.models import ApplicationReplacementHistory
from .applicant_identifier_filter import ApplicantIdentifierFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class ApplicationReplacementHistoryFilter(
    ApplicantIdentifierFilter, django_filters.FilterSet
):

    application_type = django_filters.CharFilter(
        field_name="application_type", lookup_expr="icontains"
    )

    document_number = django_filters.CharFilter(method="filter_by_document_number")

    process_name = django_filters.CharFilter(
        field_name="process_name", lookup_expr="icontains"
    )

    class Meta:
        model = ApplicationReplacementHistory
        exclude = ("historical_record",)
