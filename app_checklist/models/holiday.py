from django.db import models

from base_module.model_mixins import BaseUuidModel


class Holiday(BaseUuidModel):

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_public_holiday = models.BooleanField(default=True, help_text="Is this a public holiday?")
    holiday_date = models.DateField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    year = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"
