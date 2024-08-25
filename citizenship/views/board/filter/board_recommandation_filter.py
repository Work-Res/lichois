import django_filters
from citizenship.models import BoardRecommendation


class BoardRecommendationFilter(django_filters.FilterSet):
    recommendation = django_filters.ChoiceFilter(
        choices=[("Granted", "Granted"), ("Denied", "Denied")]
    )
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")
    reason = django_filters.CharFilter(lookup_expr="icontains")

    # Filter by interview-related fields
    interview_id = django_filters.CharFilter(
        field_name="score_sheet__interview__id", lookup_expr="exact"
    )
    interview_status = django_filters.CharFilter(
        field_name="score_sheet__interview__status", lookup_expr="icontains"
    )
    interview_date = django_filters.DateFromToRangeFilter(
        field_name="score_sheet__interview__date"
    )

    class Meta:
        model = BoardRecommendation
        fields = [
            "recommendation",
            "created_at",
            "reason",
            "interview_id",
            "interview_status",
            "interview_date",
        ]
