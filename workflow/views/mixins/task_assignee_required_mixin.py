from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from workflow.models import Task


class TaskAssigneePermission(BasePermission):
    """
    Custom permission to check that the user is both the assignee of the task
    and has the 'can_modify_task' permission.
    """

    def has_permission(self, request, view):
        # Retrieve the task based on the document_number and activity_name from the URL
        document_number = view.kwargs.get('document_number')
        activity_name = view.kwargs.get('activity_name')

        # Retrieve the task or raise 404 if not found
        task = get_object_or_404(Task, activity__name=activity_name, activity__process__document_number=document_number)

        # Check if the current user is the assignee of the task
        if task.assignee != request.user:
            raise PermissionDenied(
                "You do not have permission to edit this task's activities. You must be assigned to the task."
            )

        # Check if the user has the 'can_modify_task' permission
        if not request.user.has_perm('workflow.can_modify_task'):
            raise PermissionDenied("You do not have permission to modify tasks.")

        # If both checks pass, allow the request to proceed
        return True
