from django.db import models
from app.models import ApplicationBaseModel
from ..choices import APPLICANT_TYPE
from .employee_contract_details import EmployeeContractDetails
from .company_assets import CompanyAssets

class ExemptionCertificate(ApplicationBaseModel):

    business_name = models.CharField(max_length=150)
    employment_capacity = models.CharField(max_length=250)
    proposed_period = models.CharField(max_length=150)
    relevant_experience = models.TextField(max_length=500, blank=True, null=True)
    applicant_type = models.CharField(
        max_length=9,
        choices=APPLICANT_TYPE,
        default="employee"
    )

    employees_contracts = models.ManyToManyField(
        EmployeeContractDetails,
        related_name='contracts'
    )
    assets = models.ManyToManyField(
        CompanyAssets,
        related_name='asserts'
    )

    class Meta:
        verbose_name = "Exemption Certificate"
