import django_filters

from citizenship.models import InterviewResponse


class InterviewResponseFilter(django_filters.FilterSet):
    interview = django_filters.UUIDFilter(field_name='interview__id', lookup_expr='exact')
    member = django_filters.UUIDFilter(field_name='member', lookup_expr='exact')
    score = django_filters.NumberFilter(field_name='score', lookup_expr='exact')
    score_min = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    score_max = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    is_marked = django_filters.BooleanFilter(field_name='is_marked')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')

    # Filter by Meeting ID
    meeting = django_filters.UUIDFilter(field_name='interview__meeting__id', lookup_expr='exact')

    # Filter by Meeting Title (for example)
    meeting_title = django_filters.CharFilter(field_name='interview__meeting__title', lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and not self.data.get('member'):
            self.queryset = self.queryset.filter(member=self.request.user)

    class Meta:
        model = InterviewResponse
        fields = ['interview', 'member', 'score', 'is_marked', 'category', 'meeting', 'meeting_title']
