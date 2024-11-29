from django.db import models
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress
from app_personal_details.models import Education


class ExemptionCertificate(ApplicationBaseModel):

    business_name = models.CharField(max_length=150)
    employment_capacity = models.CharField(max_length=250)
    proposed_period = models.CharField(max_length=150)
    business_addresss = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True
    )
    qualification = models.ForeignKey(
        Education, on_delete=models.CASCADE, null=True, blank=True
    )
    experience = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Exemption Certificate"
