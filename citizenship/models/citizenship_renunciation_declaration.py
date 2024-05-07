from base_module.model_mixins import BaseUuidModel


class CitizenshipRenunciationDeclaration(BaseUuidModel):

    #Personal_details
    #Address
    #TODO: bw_citizen_declare
    #fineprint
    #TODO:declaration_signature
    #contacts_info
    #commissioner_oath

    class Meta:
        app_label = 'citizenship'
