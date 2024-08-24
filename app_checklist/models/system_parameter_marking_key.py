from datetime import timedelta
from django.db import models
from datetime import date

from base_module.model_mixins import BaseUuidModel  # type: ignore


class SystemParameterMarkingKey(BaseUuidModel):
    code = models.CharField(max_length=100, unique=True)
    pass_mark_in_percent = models.CharField(max_length=100)
    total_marks = models.CharField(max_length=100, default="100")
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField(null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = "system_parameter_marking_key"
        verbose_name = "System Parameter Marking Key"
        verbose_name_plural = "System Parameters Marking Keys"
