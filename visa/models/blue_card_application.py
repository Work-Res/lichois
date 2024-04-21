from django.db import models
from base_module.model_mixins import PersonModelMixin, PassportModelMixin
from base_module.model_mixins import ContactInfoModelMixin, AddressModelMixin
from base_module.model_mixins import DeclarationModelMixin, NationalityModelMixin
from base_module.model_mixins import CommissionerOathModelMixin, BaseUuidModel


class BlueCardApplication(BaseUuidModel, PersonModelMixin, PassportModelMixin,
                          ContactInfoModelMixin, AddressModelMixin,
                          NationalityModelMixin, DeclarationModelMixin,
                          CommissionerOathModelMixin):

    prev_bw_id = models.CharField(
        verbose_name='Previous Botswana Identity/Passport',
        max_length=15
    )

    nok_surname = models.CharField(
        verbose_name='Surname',
        max_length=150
    )

    nok_firstname = models.CharField(
        verbose_name='Firstname',
        max_length=150
    )

    nok_cell_phone = models.PositiveIntegerField(
        verbose_name='Cellphone',
    )

    nok_telephone = models.PositiveIntegerField(
        verbose_name='Telephone',
    )

    nok_relations = models.CharField(
        verbose_name='Relations',
        max_length=50
    )

    class Meta:
        app_label = 'visa'
