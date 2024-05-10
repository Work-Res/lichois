from django.db import models
from base_module.model_mixins import BaseUuidModel


class NationalityDeclaration(BaseUuidModel):

    #personal_information
    #postal_address
    #residential_address
    visit_country_name =  models.CharField(max_length=190)
    visit_country_reason = models.TextField(max_lenght=350)
    visit_country_year = models.DateField()
    #Residential_place
    #Parental_detailsx2
    #applicant_declaration
    #commissioner_oath


    class Meta:
        app_label = 'citizenship'
