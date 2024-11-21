import django_filters
from app.models import ApplicationRenewalHistory, ApplicationDocument
from ..models.application_appeal_history import ApplicationAppealHistory
from ..views.filters import ApplicantIdentifierFilter


class ApplicationAppealHistoryFilter(
    ApplicantIdentifierFilter, django_filters.FilterSet
):
    process_name = django_filters.CharFilter(
        field_name="process_name", lookup_expr="icontains"
    )
    document_number = django_filters.CharFilter(method="filter_by_document_number")

    class Meta:
        model = ApplicationAppealHistory
        exclude = ("historical_record",)
