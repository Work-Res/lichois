from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import DeclarationModelMixin
from base_module.model_mixins import CommissionerOathModelMixin


class NationalityDeclaration(CommissionerOathModelMixin,
                             DeclarationModelMixin, BaseUuidModel):

    #personal_information
    personal_info_id = models.CharField(max_length=25)

    #postal_address
    #residential_address
    address_id = models.CharField(max_length=25)

    visit_country_name = models.CharField(max_length=190)
    visit_country_reason = models.TextField(max_length=350)
    visit_country_year = models.DateField()

    #Residential_place
    place_of_residence_id = models.CharField(max_length=20)

    #Parental_detailsx2
    mother_parent_details_id = models.CharField(max_length=20)
    father_parent_details_id = models.CharField(max_length=20)

    #applicant_declaration
    #commissioner_oath


    class Meta:
        app_label = 'citizenship'
