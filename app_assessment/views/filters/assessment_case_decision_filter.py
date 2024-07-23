import django_filters

from app_assessment.models import AssessmentCaseDecision


class AssessmentCaseDecisionFilter(django_filters.FilterSet):
    parent_object_id = django_filters.UUIDFilter(field_name='parent_object_id')
    parent_object_type = django_filters.CharFilter(field_name='parent_object_type', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
    author_role = django_filters.CharFilter(field_name='author_role', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    decision = django_filters.CharFilter(field_name='decision', lookup_expr='icontains')

    class Meta:
        model = AssessmentCaseDecision
        fields = ['parent_object_id', 'parent_object_type', 'author', 'author_role', 'is_active', 'decision']
