from django.db import models
from base_module.model_mixins import BaseUuidModel


class VisaReference(BaseUuidModel):
    ref_first_name = models.CharField(
        max_length=150,
        verbose_name="First Name",
        help_text="Enter the reference's first name.",
    )
    ref_last_name = models.CharField(
        max_length=150,
        verbose_name="Last Name",
        help_text="Enter the reference's last name.",
    )
    ref_tel_no = models.CharField(
        max_length=8,
        verbose_name="Telephone Number",
        help_text="Enter the reference's 8-digit telephone number.",
    )
    ref_res_permit_no = models.PositiveIntegerField(
        verbose_name="Residence Permit Number",
        help_text="Enter the reference's residence permit number.",
    )
    ref_id_no = models.PositiveIntegerField(
        verbose_name="National ID Number",
        help_text="Enter the reference's national ID number.",
    )

    class Meta:
        app_label = "visa"
        unique_together = ("ref_first_name", "ref_res_permit_no", "ref_id_no")
        verbose_name = "Visa Reference"
        verbose_name_plural = "Visa References"
        ordering = ["ref_last_name", "ref_first_name"]

