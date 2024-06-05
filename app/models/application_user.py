from django.db import models

from base_module.model_mixins import BaseUuidModel


class ApplicationUser(BaseUuidModel):

    full_name = models.CharField(max_length=200)

    user_identifier = models.CharField(max_length=150)

    work_location_code = models.CharField(max_length=150)

    dob = models.CharField(max_length=40)

    country_cso = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.user_identifier

    class Meta:
        verbose_name_plural = "Application User"
        ordering = ['-created']
