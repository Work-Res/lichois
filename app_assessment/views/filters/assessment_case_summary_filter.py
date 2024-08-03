import django_filters

from app_assessment.models import AssessmentCaseNote, AssessmentCaseSummary


class AssessmentCaseSummaryFilter(django_filters.FilterSet):
    document_number = django_filters.CharFilter(field_name='document_number', lookup_expr='icontains')
    parent_object_id = django_filters.UUIDFilter(field_name='parent_object_id')
    parent_object_type = django_filters.CharFilter(field_name='parent_object_type', lookup_expr='icontains')
    summary = django_filters.CharFilter(field_name='summary', lookup_expr='icontains')

    class Meta:
        model = AssessmentCaseSummary
        fields = ['parent_object_id', 'parent_object_type', 'document_number', 'summary']
