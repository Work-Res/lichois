from django.db import models
from app.models import ApplicationBaseModel
from app_personal_details.models import Person
from ..choices import CITIZEN_CHOICES

class EmployeeContractDetails(ApplicationBaseModel):

    first_name = models.CharField(max_length=190, null=True, blank=True)
    last_name = models.CharField(max_length=190, null=True, blank=True)
    citizenship_status = models.CharField(max_length=11, choices=CITIZEN_CHOICES, default='citizen')
    contract_details = models.TextField()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Employee Contract Details"
