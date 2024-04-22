from django.contrib.auth.models import User
from django.db import models

from base_module.model_mixins import BaseUuidModel

from .activity import Activity


class Task(BaseUuidModel):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    group_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    details = models.TextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='tasks_participated')
    task_notes = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Task {self.id} - {self.details}"

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ['-created']
