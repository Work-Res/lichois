from base_module.model_mixins import BaseUuidModel
from django.db import models


class Naturalisation(BaseUuidModel):

    #Personal Information
    #Address
    #Spouse
    #ContactInfo

    birth_citizenship = models.CharField(max_length=190)
    present_citizenship = models.CharField(max_length=190)
    investment_level = models.CharField(max_length=190)
    prev_application_date = models.DateField()
    name_change_particulars = models.TextField(max_length=190)
    citizenship_change_particulars = models.TextField(max_length=190)
    lost_citizenship_circumstances = models.TextField(max_length=190)
    previous_convictions = models.TextField(max_length=190)
    botswana_relations = models.TextField(max_length=190)

    class Meta:
        app_label = 'citizenship'

