from authentication.models import User
from django.db import models
from simple_history.models import HistoricalRecords

from base_module.model_mixins import BaseUuidModel

from .activity import Activity
from app_checklist.models import ClassifierItem


class Task(BaseUuidModel):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    TASK_CHOICES = [
        ('NEW', 'NEW'),
        ('IN_PROGRESS', 'IN PROGRESS'),
        ('HOLD', 'ON HOLD'),
        ('CLOSED', 'CLOSED'),
    ]

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True)
    group_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks', blank=True, null=True)
    details = models.TextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='tasks_participated', blank=True,)
    task_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TASK_CHOICES)
    office_location = models.ForeignKey(ClassifierItem, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Task {self.id} - {self.details}"

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ['-created']
        permissions = [
            ("can_assign_task", "Can assign task"),
            ("can_complete_task", "Can complete task"),
            ("can_view_task", "Can view task"),
        ]
