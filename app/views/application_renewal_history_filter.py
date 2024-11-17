import django_filters
from app.models import ApplicationRenewalHistory, ApplicationDocument
from ..views.filters import ApplicantIdentifierFilter


class ApplicationRenewalHistoryFilter(
    ApplicantIdentifierFilter, django_filters.FilterSet
):
    process_name = django_filters.CharFilter(
        field_name="process_name", lookup_expr="icontains"
    )
    document_number = django_filters.CharFilter(method="filter_by_document_number")

    class Meta:
        model = ApplicationRenewalHistory
        exclude = ("historical_record",)
