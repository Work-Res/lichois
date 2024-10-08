import logging

import django_filters
from django.db.models import Q

from citizenship.models import InterviewResponse

logger = logging.getLogger(__name__)


class InterviewResponseFilter(django_filters.FilterSet):
    interview = django_filters.UUIDFilter(field_name='interview__id', lookup_expr='exact')
    member = django_filters.UUIDFilter(field_name='member__user', lookup_expr='exact')
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
        # Extract request from kwargs
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        logger.info(f"Empty empty:  {self.request.user }")

        super().__init__(*args, **kwargs)
        logger.info(f"Empty empty after:  { self.user }")

        if self.user:
            logger.info(f"Applying filter for user: {self.user}")
            # Modify the queryset to filter by the request.user
            self.filters['member'].extra.update(
                {'method': self.filter_by_request_user}
            )

    def filter_by_member(self, queryset, name, value):
        """
        Custom filter method for member field.
        If member is not provided, use request.user.
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
