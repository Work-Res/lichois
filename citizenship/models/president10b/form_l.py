from app_address.models.country import Country
from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from django.db import models

from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress
from app_personal_details.models import Person, DeceasedSpouseInfo, MarriageDissolutionInfo
from app_personal_details.models.name_change import NameChange
from citizenship.models import LocalLanguageKnowledge, ResidencyPeriod, CriminalOffense, CountryOfResidence
from citizenship.models.president10b.validators import validate_citizenship_loss_circumstances


class FormL(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    residency_periods = models.ManyToManyField(ResidencyPeriod, related_name='form_l_residency_periods')

    languages = models.ManyToManyField(LocalLanguageKnowledge, related_name='form_l_languages')

    deceased_spouse_info = models.ForeignKey(
        DeceasedSpouseInfo,
        on_delete=models.SET_NULL,
        null=True,
    )

    marriage_dissolution_info = models.ForeignKey(
        MarriageDissolutionInfo,
        on_delete=models.SET_NULL,
        null=True,
    )

    father = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_fathers"
    )

    father_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_father_address_of"
    )

    mother = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_mothers"
    )

    mother_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_mother_address_of"
    )

    previous_application_date = models.DateField(
        null=True, blank=True,
        verbose_name="Date of any previous application for registration or naturalization as a citizen of Botswana"
    )

    name_change = models.ForeignKey(
        NameChange,
        on_delete=models.SET_NULL,
        null=True,
    )

    criminal_offences = models.ManyToManyField(CriminalOffense, related_name='form_l_criminal_offences')

    countries_of_residence = models.ManyToManyField(CountryOfResidence, related_name='form_l_countries_of_residence')

    relation_description = models.TextField(
        null=True, blank=True,
        verbose_name="Any relations with Botswana (supplementary information will be required):"
    )

    sponsor = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_sponsoring_forms"
    )

    sponsor_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_sponsor_address_of"
    )

    witness = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_witnessing_persons"
    )

    witness_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_l_witness_address_of"
    )

    citizenship_loss_circumstances = models.TextField(
        blank=True, null=True,
        verbose_name="Circumstance in which Citizenship was lost." )


    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_form_l'

    def __str__(self):
        return f"FormL - {self.id}"

    def clean(self):

        validate_citizenship_loss_circumstances(
            self.present_nationality,
            self.citizenship_loss_circumstances
        )