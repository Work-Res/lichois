from django.db import models
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress


class ApplicantRelative(ApplicationBaseModel):
    surname = models.CharField(
        max_length=200,
        verbose_name="Surname",
        help_text="Enter the surname of the relative.",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="First Name",
        help_text="Enter the first name of the relative.",
    )
    relationship = models.CharField(
        max_length=200,
        verbose_name="Relationship",
        help_text="Specify the relationship to the applicant.",
    )
    address = models.ForeignKey(
        ApplicationAddress,
        on_delete=models.CASCADE,
        verbose_name="Address",
        help_text="Select the address of the relative.",
    )

    class Meta:
        app_label = "app"
        verbose_name = "Applicant Relative"
        verbose_name_plural = "Applicant Relatives"
        ordering = ["surname", "name"]

    def __str__(self):
        return f"{self.name} {self.surname} ({self.relationship})"
