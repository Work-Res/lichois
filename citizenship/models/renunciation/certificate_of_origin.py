from django.db import models

from base_module.model_mixins import BaseUuidModel

from app_personal_details.models import Person
from citizenship.models import KgosiCertificate, KgosanaCertificate


class CertificateOfOrigin(BaseUuidModel):

    father = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="fathers")

    mother = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="mothers")

    kgosi = models.ForeignKey(KgosiCertificate, on_delete=models.CASCADE, null=True, blank=True)

    kgosana = models.ForeignKey(KgosanaCertificate, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_certificate_of_origin'