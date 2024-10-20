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
    spouse_citizenship_acquired_by = models.CharField(max_length=150, blank=True, null=True)
    marriage_substiting = models.CharField(max_length=150, blank=True, null=True)
    photo_upload = models.URLField()
    known_the_applicant_for = models.IntegerField()
    date_of_declaration= models.DateField()
    signature= models.CharField(max_length=150, blank=True, null=True)
    signature_of_witness = models.CharField(max_length=150, blank=True, null=True)
    witness_last_name = models.CharField(max_length=150, blank=True, null=True)
    witness_first_name = models.CharField(max_length=150, blank=True, null=True)
    date_stamp = models.CharField(max_length=150, blank=True, null=True)
    signature_of_additional_sponsor = models.CharField(max_length=150, blank=True, null=True)
    designation_of_sponsor = models.CharField(max_length=150, blank=True,null=True)
    Signature_of_witness_to_additional_sponsor_signature = models.CharField(max_length=150, blank=True, null=True)
    place_of_declaration = models.CharField(max_length=150, blank=True, null=True)
    date_time_of_declaration = models.DateTimeField()
    commissioner_of_oaths_name = models.CharField(max_length=150, blank=True, null=True)
    designation_of_commissioner_of_oaths = models.CharField(max_length=150, blank=True, null=True)


    #parental_details_father
    #parental_details_mother


    class Meta:
        app_label = 'citizenship'
