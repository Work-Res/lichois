from django.db import models

from base_module.model_mixins import BaseUuidModel


class ApplicationUser(BaseUuidModel):

    user_identifier = models.CharField(max_length=150)

    work_location_code = models.CharField(max_length=150)

    def __str__(self):
        return self.user_identifier
