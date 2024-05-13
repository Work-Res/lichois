from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import DeclarationModelMixin
from base_module.model_mixins import CommissionerOathModelMixin


class OathOfAllegiance(DeclarationModelMixin, CommissionerOathModelMixin,
                       BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
