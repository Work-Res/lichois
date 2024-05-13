from base_module.model_mixins import BaseUuidModel
from django.db import models
from base_module.model_mixins import CommissionerOathModelMixin


class DeclarationNaturalisationByForeignSpouse(CommissionerOathModelMixin, BaseUuidModel):

    # Personal Information
    # Address
    #ContactInfo
    #ResidentialHistory
    personal_info_id = models.CharField(max_length=25)
    contact_info_id = models.CharField(max_length=25)
    address_id = models.CharField(max_length=25)
    residential_history_id = models.CharField(max_length=25)

    birth_citizenship = models.CharField(max_length=190)
    present_citizenship = models.CharField(max_length=190)
    other_prev_citizenship = models.TextField(max_length=300)
    personal_qualifications = models.TextField(max_length=500)

    #Oath

    class Meta:
        verbose_name = ('Declaration On Intention To Make An Application For A Certificate'
                        ' Of Naturalisation By A Foreign Spouse(FormK)')
        app_label = 'citizenship'
