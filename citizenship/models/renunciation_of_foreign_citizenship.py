from base_module.model_mixins import BaseUuidModel
from base_module.choices import YES_NO
from django.db import models
from ..choices import CITIZENSHIP


class RenunciationOfForeignCitizenship(BaseUuidModel):
    married = models.CharField(choices=YES_NO, max_length=3)
    spouse_first_name = models.CharField(max_length=20)
    spouse_last_name = models.CharField(max_length=20)
    spouse_middle_name = models.CharField(max_length=20)
    spouse_maiden_name = models.CharField(max_length=20)
    spouse_marriage_place = models.CharField(max_length=20)
    citizenship_by = models.CharField(choices=CITIZENSHIP, max_length=20)
    other_citizenship = models.CharField(max_length=20)
    retaining_citizenship_country = models.CharField(max_length=20)

    class Meta:
        app_label = 'citizenship'

