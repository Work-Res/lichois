from django.db import models


class AppBasePermissionModel(models.Model):
    class Meta:
        abstract = True
        permissions = [
            ('can_update_app_initial', 'Can update application'),
            ('can_delete_app_initial', 'Can delete application'),
            ('can_view_app_initial', 'Can view application'),
            ('can_view_app_replacement', 'Can view replacement application'),
            ('can_update_app_replacement', 'Can view replacement application'),
            ('can_delete_app_replacement', 'Can delete replacement application'),
            ('can_view_app_renewal', 'Can view renewal application'),
            ('can_update_app_renewal', 'Can view renewal application'),
            ('can_delete_app_renewal', 'Can delete renewal application'),
            ('can_view_app_decision', 'Can view renewal application'),
            ('can_update_app_decision', 'Can view renewal application'),
            ('can_delete_app_decision', 'Can delete renewal application'),
            ('can_view_app_minister_decision', 'Can view renewal application'),
            ('can_update_app_minister_decision', 'Can view renewal application'),
            ('can_delete_app_minister_decision', 'Can delete renewal application'),
            ('can_view_app_verification', 'Can view verification application'),
            ('can_update_app_verification', 'Can view verification application'),
            ('can_delete_app_verification', 'Can delete verification application'),
            ('can_view_app_production', 'Can view production application'),
            ('can_update_app_production', 'Can view production application'),
            ('can_delete_app_production', 'Can delete production application'),
        ]
