from django.db import models
from base_module.choices import YES_NO
from django.core.validators import MinValueValidator, MaxValueValidator
from app.models import ApplicationBaseModel

from ..choices import LANGUAGE_CHOICES

class InvestorRecord(ApplicationBaseModel):
    company_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Name of Company')
    investor_address = models.TextField(
        null=True, blank=True, verbose_name='Postal Address')
    tel = models.CharField(max_length=20, null=True, blank=True, verbose_name='Tel NO')
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name='Location of company/business(i.e'
                                                                                    'plot no. and town/village name)')

    total_asset_value = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Total Asset Value (Investment)"
    )

    citizen_employees = models.PositiveIntegerField(
        default=0,
        verbose_name="Number of Citizen Employees/Projections",
        validators=[MinValueValidator(0)]
    )

    non_citizen_employees = models.PositiveIntegerField(
        verbose_name="Number of Non-Citizen Employees (if any)",
        default=0, validators=[MinValueValidator(0)]
    )

    shares_applicant = models.DecimalField(
        verbose_name="Shares by Applicant (%)",
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    shares_botswana_partners = models.DecimalField(
        verbose_name="Shares of Botswana Partners (%)",
        blank=True, null=True,
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    names_botswana_partners = models.TextField(
        blank=True, null=True, verbose_name="Names of Batswana Partners (if any)",
    )

    non_directors = models.PositiveIntegerField(
        verbose_name="Number of Directors in the company",
        validators=[MinValueValidator(1)]
    )

    tax_registration_tin = models.CharField(
        verbose_name="BURS Tax Registration (TIN)",
        max_length=50,
    )

    cipa_number = models.CharField(
        verbose_name="CIPA Company Number",
        max_length=50
    )

    investor_permit_period = models.PositiveIntegerField(
        verbose_name="Period for which Permit is Sought (in years)",
        validators=[MinValueValidator(1)]
    )

    applicant_qualifications = models.TextField(
        blank=True, null=True, verbose_name="Qualifications of the Applicant (if any)"
    )

    bank_balance_value = models.DecimalField(
        max_digits=15, decimal_places=2,
        verbose_name="Bank Balance Value at the end of last month \
            statements also attach *Statement for 3 months*"
    )

    services_offered = models.TextField(
        null=True,
        blank=True,
        verbose_name='What services/products does your company provide'
    )

    languages_competent = models.CharField(
        choices=LANGUAGE_CHOICES, verbose_name="Languages Competent In",
        max_length=30,
    )

    language_other_specify = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="If Other, Specify Language"
    )
    residence_years = models.PositiveIntegerField(
        verbose_name="Residence in Botswana (in years)",
        validators=[MinValueValidator(0)]
    )

    capacity_employed = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Capacity in which you will be employed'
    )

    draw_salary = models.CharField(
        default='No',
        choices=YES_NO,
        max_length=3,
        verbose_name='Will you draw salary? Yes/No'
    )

    reason_draw_salary = models.TextField(
        null=True,
        blank=True,
        verbose_name='If Yes to the above question state the \
            salary (per annum) else give a reason why.'
    )
    salary_per_annum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='If yes state salary per annum'
    )
    reasons_capacity_employed = models.TextField(
        null=True,
        blank=True,
        verbose_name='If no explain why'
    )

    class Meta:
        verbose_name = "Investor Detail"
        verbose_name_plural = "Investors Details"

    def __str__(self) -> str:
        return f'{self.company_name}'
