from base_module.model_mixins import BaseUuidModel
from django.db import models


class NaturalisationOfForeignSpouse(BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
