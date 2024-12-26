from django.db import models
from app.models import ApplicationBaseModel, ApplicationDocument
from workresidentpermit.choices import YES_NO, CAPITAL_SOURCE
from app_personal_details.choices import PERSON_TYPE
from app_personal_details.models import Person, Permit
from ..choices import APPLICANT_TYPE


class VariationPermit(ApplicationBaseModel):
    existing_permit = models.ForeignKey(Permit, on_delete=models.CASCADE, verbose_name='Existing permit number')
    expiry_date = models.DateField(verbose_name='Existing permit expiry date')
    current_company_name = models.CharField(max_length=250, verbose_name='Name of the company/companies for which the current permit is held')
    new_company_name = models.CharField(max_length=250, verbose_name='Name of the proposed name company/companies for which the variation is sought')
    new_company_location = models.CharField(max_length=250, verbose_name='Location of new business/companies (i.e plot no., street, town/village)')
    has_separate_permises = models.CharField(max_length=10, choices=YES_NO, verbose_name='Does this new company/business have its own separatebusiness permises?')
    no_permises_reason = models.TextField(blank=True, null=True, verbose_name='If NO, please explain')
    new_company_services_provided = models.CharField(max_length=250, verbose_name='What services does the new company/business provide?')
    
    current_employment_capacity = models.CharField(max_length=250, verbose_name='Capacity in which presently employed')
    upcoming_employment_capacity = models.CharField(max_length=250, null=True, blank=True)
    variation_for_same_employee = models.CharField(max_length=20, choices=YES_NO, verbose_name='Is variation sought to work for the same employer')
    understudies_situation = models.TextField(null=True, blank=True, verbose_name='What is the situation regarding your understudies?')

    draw_salary = models.CharField(max_length=10, choices=YES_NO, verbose_name='Will you draw a salary?')
    salary_per_annum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='If YES, state salary per annum from this company/business. In Pula')
    new_company_employee_count = models.IntegerField(verbose_name='Number of persons to be employed by the new company/business (if any)')
    new_company_registration = models.DateField(verbose_name='When was the company registered? (Attach a photocopy of Certificate of Incorporation)')
    man_power_projection = models.TextField(verbose_name='If the company/business is currently manned by yourself only, give your manpower projections over the next five years.')
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Amount invested in company/business. In pulas.')
    initial_capital_source = models.CharField(max_length=200, choices=CAPITAL_SOURCE, verbose_name='Has initial capital been raised locally or from financial institutions outside the country?')
    financial_institution_name = models.CharField(max_length=250, verbose_name='State names of the financial institution which provided the initial capital')
    financial_institution_address = models.CharField(max_length=250, verbose_name='State addresses of the financial institution which provided the initial capital')

    subscriber = models.ForeignKey(Person, on_delete=models.CASCADE)
    person_type = models.CharField(
        max_length=50, choices=PERSON_TYPE, default="subscriber"
    )

    signature = models.CharField(max_length=150)

    applicant_type = models.CharField(
        max_length=150,
        choices=APPLICANT_TYPE,
    )
