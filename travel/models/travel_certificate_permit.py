from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import TravelCertificate


class TravelCertificatePermit(BaseUuidModel):
    certificate_number = models.ForeignKey(TravelCertificate, on_delete=models.CASCADE)
    application_submission_date = models.DateField()
    approval_date = models.DateField()
    reviewed_by_officer = models.CharField(max_length=200)
    travel_date = models.DateField()
