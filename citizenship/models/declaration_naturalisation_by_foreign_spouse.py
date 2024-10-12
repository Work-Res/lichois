from django.db import models
from app.models import ApplicationBaseModel
from base_module.model_mixins import CommissionerOathModelMixin
from citizenship.models.model_mixins.residential_history_model_mixin import ResidentialHistoryModelMixin


class DeclarationNaturalisationByForeignSpouse(ApplicationBaseModel,
                                               CommissionerOathModelMixin,
                                               ResidentialHistoryModelMixin, ):

    # Personal Information
    # Address
    #ContactInfo
    #ResidentialHistory
    # Nationality Details

    personal_qualifications = models.TextField(max_length=500)

    #Oath

    class Meta:
        verbose_name = ('Declaration On Intention To Make An Application For A Certificate'
                        ' Of Naturalisation By A Foreign Spouse(FormK)')
        app_label = 'citizenship'
