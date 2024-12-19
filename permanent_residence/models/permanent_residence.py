from django.db import models

from app.models.application_base_model import ApplicationBaseModel

from .previous_country_residence import PreviousCountryResidence


class PermanentResidence(ApplicationBaseModel):

    investor_contribution = models.CharField(max_length=255, blank=True, null=True, verbose_name='As an investor: What contribution have you made to the economy and people of Botswana? (Provide as much information as neccessary, may use additional papers)')
    employee_contribution = models.CharField(max_length=255, blank=True, null=True, verbose_name='As an employee: What contribution have you made to the economy and people of Botswana? (Provide as much information as neccessary, may use additional papers)')
    any_other_resident = models.CharField(max_length=255, blank=True, null=True, verbose_name='Any other resident: who doea not fall under (a) and (b) above: What contribution have you made to the economy and people of Botswana.(Provide as much necessary, may use additional papers.)')
    violated_terms_before = models.CharField(max_length=255, blank=True, null=True, verbose_name='During your stay in Botswana have you ever violated terms and condition of your work and/or residence permits?')
    preferred_method_comm = models.CharField(max_length=255, blank=True, null=True, verbose_name='Preffered method of communication')
    language = models.CharField(max_length=255, blank=True, null=True, verbose_name='Which languages can you read and write?')
    spouse_applying_residence = models.CharField(max_length=255, blank=True, null=True, verbose_name='Is spouse applying for permanent residence?')
    prohibited_in_botswana = models.CharField(max_length=255, blank=True, null=True)
    reasons_prohibited = models.CharField(max_length=255, blank=True, null=True)
    imprisonment_any_country = models.CharField(max_length=255, blank=True, null=True, verbose_name='Have you ever been convicted of a criminal offence in any country?')
    reasons_imprisonment = models.CharField(max_length=255, blank=True, null=True)
    permit_reasons = models.CharField(max_length=255, blank=True, null=True)
    period_when_required = models.DateField(blank=True, null=True)
    take_up_occupation = models.CharField(max_length=255, blank=True, null=True)
    application_reason = models.CharField(max_length=255, blank=True, null=True)
    application_reason_other = models.CharField(max_length=255, blank=True, null=True)
    application_status = models.CharField(max_length=255, blank=True, null=True)
    previous_country_residence = models.ManyToManyField(
        PreviousCountryResidence,
        blank=True,
        null=True
    )
