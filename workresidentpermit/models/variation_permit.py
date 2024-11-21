from django.db import models
from app.models import ApplicationBaseModel, ApplicationDocument
from workresidentpermit.choices import YES_NO, CAPITAL_SOURCE
from app_personal_details.choices import PERSON_TYPE
from app_personal_details.models import Person, Permit
from ..choices import APPLICANT_TYPE


class VariationPermit(ApplicationBaseModel):
    existing_permit = models.ForeignKey(Permit, on_delete=models.CASCADE)
    expiry_date = models.DateField()
    current_company_name = models.CharField(max_length=250)
    new_company_name = models.CharField(max_length=250)
    new_company_location = models.CharField(max_length=250)
    has_separate_permises = models.CharField(max_length=10, choices=YES_NO)
    no_permises_reason = models.TextField(blank=True, null=True)
    new_company_services_provided = models.CharField(max_length=250)
    
    current_employment_capacity = models.CharField(max_length=250)
    upcoming_employment_capacity = models.CharField(max_length=250, null=True, blank=True)
    variation_for_same_employee = models.CharField(max_length=20, choices=YES_NO)
    understudies_situation = models.TextField(null=True, blank=True)

    draw_salary = models.CharField(max_length=10, choices=YES_NO)
    salary_per_annum = models.DecimalField(max_digits=10, decimal_places=2)
    new_company_employee_count = models.IntegerField()
    new_company_registration = models.DateField()
    man_power_projection = models.TextField()
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    initial_capital_source = models.CharField(max_length=200, choices=CAPITAL_SOURCE)
    financial_institution_name = models.CharField(max_length=250)
    financial_institution_address = models.CharField(max_length=250)

    subscriber = models.ForeignKey(Person, on_delete=models.CASCADE)
    person_type = models.CharField(
        max_length=50, choices=PERSON_TYPE, default="subscriber"
    )

    signature = models.CharField(max_length=150)

    applicant_type = models.CharField(
        max_length=150,
        choices=APPLICANT_TYPE,
    )
