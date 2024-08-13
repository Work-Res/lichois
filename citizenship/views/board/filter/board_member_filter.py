import django_filters

from citizenship.models import BoardMember


class BoardMemberFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    board = django_filters.CharFilter(field_name='board__name', lookup_expr='icontains')
    board_id = django_filters.NumberFilter(field_name='board__id', lookup_expr='exact')
    role = django_filters.CharFilter(field_name='role__name', lookup_expr='icontains')

    class Meta:
        model = BoardMember
        fields = ['user', 'board', 'role']
