from django.db import models
from base_module.model_mixins import BaseUuidModel


class CitizenshipResumption(BaseUuidModel):

    personal_info_id = models.CharField(max_length=25)
    address_id = models.CharField(max_length=25)
    contact_info_id = models.CharField(max_length=25)
    father_parental_details_id = models.CharField(max_length=25)
    mother_parental_details_id = models.CharField(max_length=25)

    #TODO: form soft copy incomplete

    class Meta:
        app_label = 'citizenship'
