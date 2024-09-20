import django_filters
from citizenship.models import ScoreSheet


class ScoreSheetFilter(django_filters.FilterSet):
    interview = django_filters.CharFilter(
        field_name="interview__id", lookup_expr="exact"
    )
    board_member_representation = django_filters.CharFilter(
        field_name="board_member_representation__id", lookup_expr="exact"
    )
    total_score = django_filters.RangeFilter()
    average_score = django_filters.RangeFilter()
    passed = django_filters.BooleanFilter()
    document_number = django_filters.CharFilter(
        field_name="interview__application__application_document__document_number", lookup_expr="exact"
    )

    class Meta:
        model = ScoreSheet
        fields = [
            "interview",
            "board_member_representation",
            "total_score",
            "average_score",
            "passed",
        ]
