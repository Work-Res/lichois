from django.db import models
from base_module.model_mixins import BaseUuidModel
from .recruiters_application_decision import RecruitersApplicationDecision
from .resident_permit import ResidencePermit


class RecruitersPermit(BaseUuidModel):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=150)

    physical_address_id = models.CharField(max_length=150)
    postal_address_id = models.CharField(max_length=150)

    id_number = models.CharField(max_length=50)
    permit_type = models.CharField(max_length=150)
    permit_number = models.CharField(max_length=150)
    employment_number = models.CharField(max_length=150)
    education_qualification = models.CharField(max_length=150)
    work_experience = models.CharField(max_length=150)
    salary = models.DecimalField(decimal_places=2)
    payment_mode = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=150)
    signed_date = models.DateField()
    applicant_signature = models.CharField(max_length=150)
    recruiters_signed_date = models.DateField()
    recruiters_names = models.CharField(max_length=250)
    recruiters_position = models.CharField(max_length=150)
    recruiters_signature = models.CharField(max_length=150)

    work_resident_permit = models.ForeignKey(ResidencePermit, on_delete=models.CASCADE)
    recruiters_application_decision = models.ForeignKey(
        RecruitersApplicationDecision, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Child"
