from django.db import models
# from base_module.model_mixins import PersonModelMixin, PassportModelMixin
# from base_module.model_mixins import ContactInfoModelMixin, AddressModelMixin
from base_module.model_mixins import DeclarationModelMixin #, NationalityModelMixin
from base_module.model_mixins import CommissionerOathModelMixin
from base_module.model_mixins import BaseUuidModel


class BlueCardApplication(CommissionerOathModelMixin,
                          DeclarationModelMixin, BaseUuidModel):

    personal_info_id = models.CharField(max_length=25)
    passport_details_id = models.CharField(max_length=25)
    contact_info_id = models.CharField(max_length=25)
    address_id = models.CharField(max_length=25)

    prev_bw_id = models.CharField(max_length=15)
    nok_surname = models.CharField(max_length=150)
    nok_firstname = models.CharField(max_length=150)
    nok_cell_phone = models.PositiveIntegerField()
    nok_telephone = models.PositiveIntegerField()
    nok_relations = models.CharField(max_length=50)

    class Meta:
        app_label = 'visa'
