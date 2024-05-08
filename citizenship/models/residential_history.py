from django.db import models
from base_module.model_mixins import BaseUuidModel


class ResidentialHistory(BaseUuidModel):

    country = models.CharField(max_length=190)

    residency_from = models.DateField(
        #validation=DateNotFuture
    )

    residency_to = models.DateField(
        # validation=DateNotFuture
    )

    class Meta:
        app_label = 'citizenship'
