from base_module.model_mixins import BaseUuidModel


class CitizenshipBySettlement(BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
