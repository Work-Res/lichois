import django_filters

from app_assessment.models import AssessmentCaseNote


class AssessmentCaseNoteFilter(django_filters.FilterSet):
    parent_object_id = django_filters.UUIDFilter(field_name='parent_object_id')
    parent_object_type = django_filters.CharFilter(field_name='parent_object_type', lookup_expr='icontains')
    note_text = django_filters.CharFilter(field_name='note_text', lookup_expr='icontains')
    note_type = django_filters.CharFilter(field_name='note_type', lookup_expr='icontains')

    class Meta:
        model = AssessmentCaseNote
        fields = ['parent_object_id', 'parent_object_type', 'note_text', 'note_type']
