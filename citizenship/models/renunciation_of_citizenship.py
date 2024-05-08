from base_module.model_mixins import BaseUuidModel
from base_module.choices import YES_NO
from django.db import models


class RenunciationOfCitizenship(BaseUuidModel):

    renounce_citizenship = models.CharField(choices=YES_NO, max_length=3)

    class Meta:
        app_label = 'citizenship'
