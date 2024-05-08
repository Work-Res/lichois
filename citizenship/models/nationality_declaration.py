from base_module.model_mixins import BaseUuidModel


class NationalityDeclaration(BaseUuidModel):

    class Meta:
        app_label = 'citizenship'
