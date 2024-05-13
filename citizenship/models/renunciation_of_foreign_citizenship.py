from base_module.model_mixins import BaseUuidModel
from django.db import models
from ..choices import CITIZENSHIP_OPTIONS
from base_module.model_mixins import DeclarationModelMixin
from base_module.model_mixins import CommissionerOathModelMixin


class RenunciationOfForeignCitizenship(CommissionerOathModelMixin,
                                       DeclarationModelMixin, BaseUuidModel):

    #personal_details
    personal_info_id = models.CharField(max_length=25)
    # spouse_info
    spouse_info_id = models.CharField(max_length=25)
    # Contacts_info
    contact_info_id = models.CharField(max_length=25)
    # postal_address
    # residential_address
    address_id = models.CharField(max_length=25)

    bw_citizenship_by = models.CharField(choices=CITIZENSHIP_OPTIONS, max_length=20)
    other_citizenship_country = models.CharField(max_length=50)
    other_citizenship_by = models.CharField(choices=CITIZENSHIP_OPTIONS, max_length=20)
    renunciation_country = models.CharField(max_length=50)
    employment = models.TextField(max_length=250)
    #Oath

    oath_of_allegiance_id = models.CharField(max_length=25)

    class Meta:
        app_label = 'citizenship'

