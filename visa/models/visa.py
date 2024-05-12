from django.db import models
from base_module.model_mixins import BaseUuidModel


class Visa(BaseUuidModel):

    class Meta:
        app_label = 'visa'