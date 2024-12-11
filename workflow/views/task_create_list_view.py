from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from workflow.models import Task
from .mixins.custom_permission_required import CustomPermissionRequired
from ..views import TaskFilter

from workflow.api.serializers import TaskSerializer


class TaskCreateListViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    ordering_fields = (
        'created',
    )

    # method-level permissions
    method_permissions = {
        'list': ['app.can_view_app_initial'],
        'retrieve': ['app.can_view_app_initial'],
        'claim': ['workflow.wfm_can_assign_task'],
        'unassign': ['workflow.wfm_can_unassigned_task'],
        'change_status': ['workflow.wfm_can_change_task_status'],  # Added
        'assign_to_user': ['workflow.wfm_can_assign_task'],  # Added
    }
    method_permissions = {}

    def get_permissions(self):
        """
        Get the appropriate permissions for the current action.
        """
        permissions = [IsAuthenticated()]  # Default permission
        method_permission_codes = self.method_permissions.get(self.action, [])
        if method_permission_codes:
            self.required_permissions = method_permission_codes  # Set required_permissions dynamically
            permissions.append(CustomPermissionRequired())
        return permissions

    @action(detail=True, methods=['post'], permission_classes=[])
    def claim(self, request, pk=None):
        """POST /api/tasks/{id}/claim/
        """
        try:
            task = self.get_object()
            task.assignee = request.user
            task.save()
            return Response(
                {"detail": "Task claimed successfully."},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[])
    def unassign(self, request, pk=None):
        """POST /api/tasks/{id}/unassign/
        """
        try:
            task = self.get_object()
            task.assignee = None
            task.save()
            return Response(
                {"detail": "Task unassigned successfully."},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[])
    def change_status(self, request, pk=None):
        try:
            task = self.get_object()
            new_status = request.data.get('status')
            if new_status not in dict(Task.TASK_CHOICES).keys():
                return Response(
                    {"detail": "Invalid status value."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            task.status = new_status
            task.save()
            return Response(
                {"detail": f"Task status changed to {new_status} successfully."},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[])
    def assign_to_user(self, request, pk=None):
        try:
            task = self.get_object()
            user_id = request.data.get('user_id')
            username = request.data.get('username')

            # Find user by user_id or username
            if user_id:
                user = User.objects.filter(id=user_id).first()
            elif username:
                user = User.objects.filter(username=username).first()
            else:
                return Response(
                    {"detail": "Please provide either user_id or username."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user:
                return Response(
                    {"detail": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            task.assignee = user
            task.save()
            return Response(
                {"detail": f"Task assigned to {user.username} successfully."},
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )
