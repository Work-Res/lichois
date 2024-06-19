from django.db import models

from base_module.model_mixins import BaseUuidModel # type: ignore


class SystemParameter(BaseUuidModel):

    DURATION_TYPE_CHOICES = [
        ('years', 'Year(s)'),
        ('months', 'Month(s)'),
        ('weeks', 'Week(s)'),
    ]

    duration_type = models.CharField(
        max_length=6,
        choices=DURATION_TYPE_CHOICES,
        default='years',
    )
    duration = models.IntegerField()
    application_type = models.CharField(max_length=255)
    valid_from = models.DateField()
    valid_to = models.DateField()

    class Meta:
        db_table = 'system_parameter'
        verbose_name = 'System Parameter'
        verbose_name_plural = 'System Parameters'
