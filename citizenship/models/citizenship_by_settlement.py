from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import CommissionerOathModelMixin
from base_module.model_mixins import DeclarationModelMixin


class CitizenshipBySettlement(CommissionerOathModelMixin,
                              DeclarationModelMixin, BaseUuidModel):
    # personal_information
    personal_info_id = models.CharField(max_length=25)

    # contact_information
    contact_info_id = models.CharField(max_length=25)
    # physical_address
    # postal_address
    address_id = models.CharField(max_length=25)

    #personal_declaration actual application?

    #KgosiCert
    kgosi_cert_id = models.CharField(max_length=25)
    #KgosanaCert
    kgosana_cert_id = models.CharField(max_length=25)
    #CommissionerOath
    #DCCertificate
    dc_certificate_id = models.CharField(max_length=25)



    class Meta:
        app_label = 'citizenship'
