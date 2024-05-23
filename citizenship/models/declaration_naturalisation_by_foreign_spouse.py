from django.db import models
from app.models import ApplicationBaseModel
from base_module.model_mixins import CommissionerOathModelMixin


class DeclarationNaturalisationByForeignSpouse(CommissionerOathModelMixin, ApplicationBaseModel):

    # Personal Information
    # Address
    #ContactInfo

    #TODO: link residential history
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
