from django.db import models
from base_module.model_mixins import BaseUuidModel
from .model_mixins import PersonalDetailsModelMixin


class CitizenSponsorCertificate(PersonalDetailsModelMixin, BaseUuidModel):

    #firstname

    #lastname
    # postal_address

    # residential_address

    applicant_known_years = models.PositiveIntegerField()

    declaration_date = models.DateField()

    declaration_sign = models.CharField(max_length=15)

    #witness_details

    class Meta:
        app_label = 'citizenship'
