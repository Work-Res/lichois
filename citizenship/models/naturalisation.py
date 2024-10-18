from base_module.model_mixins import BaseUuidModel
from django.db import models


class Naturalisation(BaseUuidModel):

    # Personal Information
    personal_info_id = models.CharField(max_length=25)

    # ContactInfo
    contact_info_id = models.CharField(max_length=25)

    # Address
    address_id = models.CharField(max_length=25)

    # Spouse
    spouse_info_id = models.CharField(max_length=25)

    birth_citizenship = models.CharField(max_length=190)
    present_citizenship = models.CharField(max_length=190)
    investment_level = models.CharField(max_length=190)
    prev_application_date = models.DateField()
    name_change_particulars = models.TextField(max_length=190)
    citizenship_change_particulars = models.TextField(max_length=190)
    lost_citizenship_circumstances = models.TextField(max_length=190)
    previous_convictions = models.TextField(max_length=190)
    botswana_relations = models.TextField(max_length=190)
    period_of_residence_in_bw_from = models.CharField(max_length=190)
    period_of_residence_in_bw_until = models.CharField(max_length=190)
    occupation = models.CharField(max_length=190)
    qualifications = models.CharField(max_length=190)
    date_of_marriage = models.CharField(max_length=190)
    country_of_dissolution = models.CharField(max_length=190)
    place_of_dissolution = models.CharField(max_length=190)
    date_of_dissolution = models.DateField()
    father_citizenship_at_time_of_death = models.CharField(max_length=190)
    mother_citizenship_at_time_of_death = models.CharField(max_length=190)
    date_of_any_previous_application_for_naturalization_as_citizen_of_Botswana = models.CharField(max_length=190)
    signature_of_applicant = models.CharField(max_length=190)
  



    class Meta:
        app_label = 'citizenship'

