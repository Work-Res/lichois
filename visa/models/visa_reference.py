from django.db import models
from base_module.model_mixins import BaseUuidModel


class VisaReference(BaseUuidModel):
    ref_first_name = models.CharField(max_length=150)

    ref_last_name = models.CharField(max_length=150)

    ref_tel_no = models.CharField(max_length=8)

    ref_res_permit_no = models.PositiveIntegerField()

    ref_id_no = models.PositiveIntegerField()

    class Meta:
        app_label = "visa"
        unique_together = ("ref_first_name", "ref_res_permit_no", "ref_id_no")
