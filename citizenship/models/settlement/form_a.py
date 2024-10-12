from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from django.db import models

from app.models import ApplicationBaseModel
from .kgosi_certificate import KgosiCertificate
from .kgosana_certificate import KgosanaCertificate
from .DC_certificate import DCCertificate

from .preferred_comm_choices import COMMUNICATION_CHOICES


class FormA(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    kgosi_certificate = models.ForeignKey(
        KgosiCertificate, on_delete=models.CASCADE, null=True, blank=True, related_name="kgosi")

    kgosana_certificate = models.ForeignKey(
        KgosanaCertificate, on_delete=models.CASCADE, null=True, blank=True, related_name="kgosana")

    preferred_method_of_comm = models.CharField(max_length=100, choices=COMMUNICATION_CHOICES)

    dc_certificate = models.ForeignKey(
        DCCertificate, on_delete=models.CASCADE, null=True, blank=True, related_name="declarant")

    tribe_ordinarily_community_kgosi = models.CharField(max_length=100, null=True, blank=True)

    tribe_customarily_community_kgosi = models.CharField(max_length=100, null=True, blank=True)

    tribe_ordinarily_community_kgosana = models.CharField(max_length=100, null=True, blank=True)

    tribe_customarily_community_kgosana = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_form_a'
