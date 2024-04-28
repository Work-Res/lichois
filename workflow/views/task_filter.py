from django_filters import rest_framework as filters
from django_filters import AllValuesFilter

from ..models import Task


class TaskFilter(filters.FilterSet):

    created_from = filters.DateTimeFilter(field_name="created", lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name="created", lookup_expr='lte')
    activity_name = AllValuesFilter(field_name='activity__name')
    office_name = AllValuesFilter(field_name='office_location__name')
    assignee_name = AllValuesFilter(field_name='assignee__username')

    class Meta:
        model = Task
        fields = (
            'priority',
            'assignee',
            'office_name',
            'activity_name',
            'office_name',
            'status',
            'created_from',
            'created_to',
            'assignee_name'
        )
