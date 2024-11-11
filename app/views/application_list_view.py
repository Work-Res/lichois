from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from app.models import Application
from app.api.serializers import ApplicationSerializer
from app.views.filters.application_filter import ApplicationModelFilter
from rest_framework.exceptions import ValidationError

from workflow.views.mixins.custom_permission_required import CustomPermissionRequired
from workflow.views.mixins.task_assignee_required_mixin import TaskAssigneePermission


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class ApplicationListView(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationModelFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [TaskAssigneePermission, CustomPermissionRequired]
    required_permissions = ['app.can_view_app_initial', 'app.can_view_app_replacement', 'app.can_view_app_renewal']

    def get_queryset(self):
        queryset = self.queryset
        sort_by = self.request.query_params.get('sort_by', 'created')
        order_by = self.request.query_params.get('order', 'asc')

        allowed_sort_fields = ['created']

        if sort_by and sort_by not in allowed_sort_fields:
            raise ValidationError(f"Invalid sort field: {sort_by}")

        if order_by not in ['asc', 'desc']:
            raise ValidationError(f"Invalid order value: {order_by}")

        if sort_by:
            if order_by == 'desc':
                sort_by = f'-{sort_by}'
            else:
                sort_by = sort_by

        return queryset.order_by(sort_by)
