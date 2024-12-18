from django.db import models
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress
from app_personal_details.models import Education


class ExemptionCertificate(ApplicationBaseModel):

    business_name = models.CharField(max_length=150,verbose_name='Name of business/Undertaking/Organisation')
    business_addresss = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,verbose_name="Address"
    )
    employment_capacity = models.CharField(max_length=250,verbose_name='Capacity in which employed')
    qualification = models.ForeignKey(
        Education, on_delete=models.CASCADE, null=True, blank=True
    )
    experience = models.CharField(max_length=250, null=True, blank=True)
    proposed_period = models.CharField(max_length=150,verbose_name="State proposed period of engagement")

    class Meta:
        verbose_name = "Exemption Certificate"
