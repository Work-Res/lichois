from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import CommissionerOathModelMixin, DeclarationModelMixin


class CitizenshipRenunciationDeclaration(CommissionerOathModelMixin,
                                         DeclarationModelMixin, BaseUuidModel):

    #Personal_details
    personal_info_id = models.CharField(max_length=25)
    #Address
    address_id = models.CharField(max_length=25)
    #TODO: bw_citizen_declare

    #fineprint
    #TODO:declaration_signature

    #contacts_info
    contact_info_id = models.CharField(max_length=25)

    #commissioner_oath

    class Meta:
        app_label = 'citizenship'
