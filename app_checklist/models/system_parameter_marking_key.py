from datetime import timedelta
from django.db import models
from datetime import date

from base_module.model_mixins import BaseUuidModel  # type: ignore


class SystemParameter(BaseUuidModel):

    DURATION_TYPE_CHOICES = [
        ("years", "Year(s)"),
        ("months", "Month(s)"),
        ("weeks", "Week(s)"),
        ("days", "Days(s)"),
        ("permanent", "Permanent"),
    ]

    duration_type = models.CharField(
        max_length=100,
        choices=DURATION_TYPE_CHOICES,
    )
    duration = models.IntegerField(null=True, blank=True)
    application_type = models.CharField(max_length=255)
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField(null=True, blank=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.valid_to:
            self.valid_to = date.today() + timedelta(days=365 * self.duration)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "system_parameter"
        verbose_name = "System Parameter"
        verbose_name_plural = "System Parameters"
