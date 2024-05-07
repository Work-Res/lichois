from base_module.model_mixins import BaseUuidModel
from django.db import models
from ..choices import CITIZENSHIP_OPTIONS


class RenunciationOfForeignCitizenship(BaseUuidModel):

    #personal_details
    #postal_address
    #residential_address
    #spouse_info
    #Contacts_info

    bw_citizenship_by = models.CharField(choices=CITIZENSHIP_OPTIONS, max_length=20)
    other_citizenship_country = models.CharField(max_length=50)
    other_citizenship_by = models.CharField(choices=CITIZENSHIP_OPTIONS, max_length=20)
    renunciation_country = models.CharField(max_length=50)
    employment = models.TextField(max_length=250)

    #Oath
    #Oath_of_allegiance

    class Meta:
        app_label = 'citizenship'

