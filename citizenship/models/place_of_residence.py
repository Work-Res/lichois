from base_module.model_mixins import BaseUuidModel
from django.db import models


class PlaceOfResidence(BaseUuidModel):

    age_from = models.PositiveIntegerField()
    age_to = models.PositiveIntegerField()
    parent_guardian = models.CharField(max_length=250)
    place_name = models.CharField(max_length=150)

    class Meta:
        app_label = 'citizenship'
