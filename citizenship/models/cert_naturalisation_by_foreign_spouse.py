from base_module.model_mixins import BaseUuidModel
from django.db import models


class CertNaturalisationByForeignSpouse(BaseUuidModel):

    #PersonalDetails
    #Address
    #ContactInfo
    #SpouseInfo
    #parental_details

    #TODO: (declarations)
    #full_age_capacity
    #not_remarried
    #not_late_lodging
    #not_been_resident
    #apply_naturalisation
    marriage_date = models.DateField(blank=True, null=True)
    marriage_country = models.CharField(max_length=150, blank=True, null=True)
    marriage_place = models.CharField(max_length=150, blank=True, null=True)
    prev_surname = models.CharField(max_length=150, blank=True, null=True)
    prev_firstname = models.CharField(max_length=150, blank=True, null=True)
    prev_middlename = models.CharField(max_length=150, blank=True, null=True)
    prev_maidenname = models.CharField(max_length=150, blank=True, null=True)
    citizenship = models.CharField(max_length=150, blank=True, null=True)
    continued_residence_from = models.DateField()
    continued_residence_to = models.DateField(blank=True, null=True)

    #parental_details_father
    #parental_details_mother


    class Meta:
        app_label = 'citizenship'
