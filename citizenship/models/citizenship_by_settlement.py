from base_module.model_mixins import BaseUuidModel


class CitizenshipBySettlement(BaseUuidModel):

    #personal_information
    #physical_address
    #postal_address
    #contact_information
    #personal_declaration actual application?
    #KgosiCert
    #KgosanaCert
    #CommissionerOath
    #DCCertificate
    #ApplicantDeclaration


    class Meta:
        app_label = 'citizenship'
