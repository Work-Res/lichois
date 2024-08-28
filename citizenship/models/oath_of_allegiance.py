from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import DeclarationModelMixin
from base_module.model_mixins import CommissionerOathModelMixin

from app.models import ApplicationBaseModel


class OathOfAllegiance(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    class Meta:
        app_label = 'citizenship'
