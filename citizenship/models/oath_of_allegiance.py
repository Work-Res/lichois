from django.db import models
from base_module.model_mixins import BaseUuidModel


class OathOfAllegiance(BaseUuidModel):
    #TODO: oath of allegiance
    class Meta:
        app_label = 'citizenship'
