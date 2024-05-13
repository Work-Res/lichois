from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import DeclarationModelMixin
from base_module.model_mixins import CommissionerOathModelMixin


class AdoptedChildRegistration(CommissionerOathModelMixin,
                               DeclarationModelMixin, BaseUuidModel):

    # applicant_personal_info
    personal_info_id = models.CharField(max_length=25)

    #child_personal_info
    child_personal_info_id = models.CharField(max_length=25)
    address_id = models.CharField(max_length=25)
    contact_info_id = models.CharField(max_length=25)
    adoptive_father_details_id = models.CharField(max_length=25)
    adoptive_mother_details_id = models.CharField(max_length=25)
    citizen_sponsor1_id = models.CharField(max_length=25)
    citizen_sponsor2_id = models.CharField(max_length=25)

    class Meta:
        app_label = 'citizenship'
