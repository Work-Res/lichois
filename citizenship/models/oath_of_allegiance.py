from django.db import models
from base_module.model_mixins import BaseUuidModel


class OathOfAllegiance(BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
