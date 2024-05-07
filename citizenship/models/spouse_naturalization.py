from base_module.model_mixins import BaseUuidModel
from django.db import models


class SpouseNaturalization(BaseUuidModel):
    maiden_name = models.CharField(
        verbose_name='Previous/Maiden Surname',
        max_length=190, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    cell_phone_number = models.CharField(max_length=8, blank=True, null=True)
    tel_phone_number = models.CharField(max_length=8, blank=True, null=True)

    citizenship_at_birth = models.CharField(
        verbose_name='Citizenship at Birth',
        max_length=20)

    current_citizenship = models.CharField(
        verbose_name='Present Citizenship (if different)',
        max_length=20, blank=True, null=True)

    qualification = models.TextField(blank=True, null=True)

    contribution_or_investment = models.TextField(blank=True, null=True,
                                                  help_text='Provide details in a separate sheet')
    date_of_marriage = models.DateField()

    # spouse info
    spouse_firstname = models.CharField(max_length=40)
    spouse_lastname = models.CharField(max_length=40)
    spouse_middle = models.CharField(max_length=40)
    spouse_maiden_name = models.CharField(
        verbose_name='Previous/Maiden Surname',
        max_length=190, blank=True, null=True)

    # if spouse deceased
    spouse_country_of_death = models.CharField(max_length=20)
    spouse_place_of_death = models.CharField(max_length=20)
    spouse_date_of_death = models.CharField(max_length=20)

    # spouse qualification
    spouse_academic_or_profession = models.CharField(max_length=20, blank=True, null=True)
    spouse_qualification_desc = models.TextField(blank=True, null=True)

    # if marriage is dissolved
    country_of_dissolution = models.CharField(max_length=20, blank=True, null=True)
    place_of_dissolution = models.CharField(max_length=20, blank=True, null=True)
    date_of_dissolution = models.DateField(blank=True, null=True)

    # father details


class InlinePeriod(models.Model):
    naturalization = models.ForeignKey(Naturalisation, on_delete=models.DO_NOTHING)
    start_date = models.DateField(verbose_name='Period from')
    end_date = models.DateField(verbose_name='Period Unitl')


class InlineLanguages(models.Model):
    naturalization = models.ForeignKey(Naturalisation, on_delete=models.DO_NOTHING)
    name = models.CharField(verbose_name='Languages', max_length=20)
