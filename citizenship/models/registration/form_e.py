from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from django.db import models

from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress
from app_personal_details.models import Person
from base_module.choices import YES_NO


class FormE(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    guardian = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="child_relations"
    )

    citizenship_at_birth = models.CharField(
        max_length=10, choices=YES_NO, blank=True, null=True,
        verbose_name="Citizenship at birth"
    )

    present_citizenship = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Present citizenship (if different)"
    )

    present_citizenship_not_available = models.CharField(
        max_length=10, choices=YES_NO, blank=True, null=True,
        verbose_name="Do you have present citizenship?"
    )

    provide_circumstances = models.CharField(
        max_length=300, blank=True, null=True,
        verbose_name="If no present citizenship, circumstances under which it was lost"
    )

    father = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="father_of"
    )

    father_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="father_address_of"
    )

    mother = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="mother_of"
    )

    mother_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="mother_address_of"
    )

    sponsor = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="sponsoring_forms"
    )

    sponsor_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="sponsor_address_of"
    )

    is_sponsor_signed = models.BooleanField(
        verbose_name="Sponsor Signature"
    )

    sponsor_date_of_signature = models.DateField(
        null=True, blank=True, verbose_name="Date of Sponsor's Signature"
    )

    witness = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="witnessing_persons"
    )

    witness_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="witness_address_of"
    )

    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_form_e'

    def __str__(self):
        return f"Form E - {self.id}"