from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.choices import GENDER
from .exemption_cert_application import ExemptionCertificateApplication


class ExemptionCertificateDependant(BaseUuidModel):

    exempt_cert_application = models.ForeignKey(ExemptionCertificateApplication, on_delete=models.CASCADE)
    dependant_fname = models.CharField(max_length=150)
    dependant_lname = models.CharField(max_length=150)
    dependant_age = models.PositiveIntegerField()
    dependant_gender = models.CharField(choices=GENDER, max_length=6)

    class Meta:
        app_label = 'visa'
        unique_together = ('exempt_cert_application__id', 'dependant_fname',
                           'dependant_lname', 'dependant_age')
