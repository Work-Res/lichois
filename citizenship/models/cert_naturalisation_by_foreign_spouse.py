from base_module.model_mixins import BaseUuidModel
from django.db import models


class CertNaturalisationByForeignSpouse(BaseUuidModel):

    #PersonalDetails
    #Address
    #ContactInfo
    #SpouseInfo

    class Meta:
        app_label = 'citizenship'
