from django.db import models
from base_module.model_mixins import PersonModelMixin, PassportModelMixin
from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from base_module.model_mixins import BaseUuidModel
from lichois.visa.choices import PERIOD_MEASURE


class ExemptionCertificateApplication(BaseUuidModel, PersonModelMixin, PassportModelMixin,
                                      DeclarationModelMixin, CommissionerOathModelMixin):

    business_name = models.CharField(
        verbose_name='Name of Business/Undertaking/Organisation',
        max_length=150
    )

    # address?

    employment_capacity = models.CharField(
        verbose_name='Capacity in which employed',
        max_length=150
    )

    qualification_experience = models.TextField(
        verbose_name='Qualification and/or experience',
        max_length=500
    )

    engagement_period = models.PositiveIntegerField(
        verbose_name='State proposed period of engagement'
    )

    engagement_period_measure = models.CharField(
        choices=PERIOD_MEASURE,
        max_length=10
    )

    class Meta:
        app_label = 'visa'


