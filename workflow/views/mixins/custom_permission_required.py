from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied


class CustomPermissionRequired(BasePermission):

    """
    Custom permission class to check if a user has all the required permissions for the view.
    """

    def has_permission(self, request, view):
        # The required permissions can be defined as a list on the view class, e.g., view.required_permissions
        required_permissions = getattr(view, 'required_permissions', None)

        if required_permissions is None:
            # No specific permissions required for this view
            return True

        if isinstance(required_permissions, str):
            required_permissions = [required_permissions]

        missing_permissions = [perm for perm in required_permissions if not request.user.has_perm(perm)]
        if missing_permissions:
            raise PermissionDenied(f"You do not have the required permissions.")

        return True
