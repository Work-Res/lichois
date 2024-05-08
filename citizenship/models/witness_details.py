from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class WitnessDetails(PersonalDetailsModelMixin, BaseUuidModel):

    # firstname

    # lastname
    # postal_address

    # residential_address

    class Meta:
        app_label = 'citizenship'
