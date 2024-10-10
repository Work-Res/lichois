import logging

import django_filters
from django.db.models import Q

from citizenship.models import InterviewResponse

logger = logging.getLogger(__name__)


class InterviewResponseFilter(django_filters.FilterSet):
    interview = django_filters.UUIDFilter(field_name='interview__id', lookup_expr='exact')
    member = django_filters.UUIDFilter(method='filter_by_member')  # Custom method applied here
    score = django_filters.NumberFilter(field_name='score', lookup_expr='exact')
    score_min = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    score_max = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    is_marked = django_filters.BooleanFilter(field_name='is_marked')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')

    # Filter by Meeting ID
    meeting = django_filters.UUIDFilter(field_name='interview__meeting__id', lookup_expr='exact')

    # Filter by Meeting Title
    meeting_title = django_filters.CharFilter(field_name='interview__meeting__title', lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        # Extract the request object from kwargs
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super().__init__(*args, **kwargs)

        if self.request:
            logger.info(f"Request user: {self.request.user}")

    def filter_by_member(self, queryset, name, value):
        """
        Custom filter method for the 'member' field.
        If the 'member' value is provided in the query params, it filters by that.
        Otherwise, it filters by the current request user.
        """
        if value:
            return queryset.filter(member__user=value)
        if self.request:
            logger.info(f"Filtering by request user: {self.user}")
            return queryset.filter(member__user=self.user)
        return queryset

    class Meta:
        model = InterviewResponse
        fields = ['interview', 'member', 'score', 'is_marked', 'category', 'meeting', 'meeting_title']