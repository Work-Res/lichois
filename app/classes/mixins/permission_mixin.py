from rest_framework.permissions import IsAuthenticated
from ..permissions import CustomPermissionRequired


class PermissionMixin:
    """
    Mixin to handle method-level permissions.
    """
    method_permissions = {}

    def get_permissions(self):
        """
        Dynamically set permissions based on the action being performed.
        """
        permissions = [IsAuthenticated()]  # Default permission
        method_permission_codes = self.method_permissions.get(self.action, [])
        if method_permission_codes:
            self.required_permissions = method_permission_codes  # Dynamically set required permissions
            permissions.append(CustomPermissionRequired())
        return permissions
