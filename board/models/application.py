from django.db import models
from base_module.model_mixins import BaseUuidModel


class Application(BaseUuidModel):
    application_id = models.CharField(max_length=250)

    def __str__(self):
        return self.application_id

