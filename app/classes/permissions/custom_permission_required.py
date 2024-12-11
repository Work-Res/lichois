from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied


class CustomPermissionRequired(BasePermission):
    """
    Custom permission class to check if a user has all the required permissions for the view.
    """

    def __init__(self, permission_codes=None):
        self.permission_codes = permission_codes or []

    def has_permission(self, request, view):
        # Use the permissions passed during instantiation or from the view
        required_permissions = self.permission_codes or getattr(view, 'required_permissions', None)

        if not required_permissions:
            # No specific permissions required for this view
            return True

        if isinstance(required_permissions, str):
            required_permissions = [required_permissions]

        missing_permissions = [perm for perm in required_permissions if not request.user.has_perm(perm)]
        if missing_permissions:
            raise PermissionDenied(f"You do not have the required permissions: {', '.join(missing_permissions)}.")

        return True
