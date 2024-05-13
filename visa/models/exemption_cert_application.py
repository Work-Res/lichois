from django.db import models
# from base_module.model_mixins import PersonModelMixin, PassportModelMixin
# from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from base_module.model_mixins import BaseUuidModel
from ..choices import PERIOD_MEASURE


class ExemptionCertificateApplication(BaseUuidModel):

    personal_info_id = models.CharField(max_length=25)
    passport_details_id = models.CharField(max_length=25)
    contact_info_id = models.CharField(max_length=25)
    address_id = models.CharField(max_length=25)

    business_name = models.CharField(max_length=150)
    employment_capacity = models.CharField(max_length=250)
    proposed_period = models.PositiveIntegerField()
    status = models.CharField(max_length=250)
    applicant_signature = models.TextField(max_length=250)
    application_date = models.DateField()
    commissioner_signature = models.CharField(max_length=250)

    class Meta:
        app_label = 'visa'


