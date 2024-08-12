import django_filters

from citizenship.models import Board


class BoardFilter(django_filters.FilterSet):
    meeting_id = django_filters.UUIDFilter(field_name='board_meetings__id', lookup_expr='exact')

    class Meta:
        model = Board
        fields = ['meeting_id']
