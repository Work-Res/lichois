from django.db import models


class AppBasePermissionModel(models.Model):
    class Meta:
        abstract = True
        permissions = [
            ('can_assign_task', 'Can assign Task'),
            ('can_claim_task', 'Can claim Task'),
            ('can_unassigned_task', 'Can unassigned Task')
            ('can_change_task_status', 'Can change Task status')
        ]
