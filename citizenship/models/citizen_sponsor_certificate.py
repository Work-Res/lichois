from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class CitizenSponsorCertificate(PersonalDetailsModelMixin, BaseUuidModel):

    personal_info_id = models.CharField(max_length=25)
    postal_address_id = models.CharField(max_length=25)
    # residential_address_id

    applicant_known_years = models.PositiveIntegerField()
    declaration_date = models.DateField()
    declaration_sign = models.CharField(max_length=15)
    witness1_details_id = models.CharField(max_length=25)
    witness2_details_id = models.CharField(max_length=25)

    class Meta:
        app_label = 'citizenship'
