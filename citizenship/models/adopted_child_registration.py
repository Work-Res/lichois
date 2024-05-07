from base_module.model_mixins import BaseUuidModel


class AdoptedChildRegistration(BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
