from django.db import models
from app.models import ApplicationBaseModel
from base_module.choices import YES_NO


class Spouse(ApplicationBaseModel):
    last_name = models.CharField(max_length=190,verbose_name="Last Name")
    first_name = models.CharField(max_length=190,verbose_name="First Name")
    middle_name = models.CharField(max_length=190, blank=True, null=True,verbose_name="Other Names")
    maiden_name = models.CharField(max_length=190, blank=True, null=True,verbose_name="Previous/Maiden Surname")
    country = models.CharField(max_length=190,verbose_name="Country of Birth of Spouse")
    place_birth = models.CharField(max_length=190,verbose_name="Place of Birth of Spouse")
    dob = models.DateField(verbose_name="Date of Birth of Spouse")
    is_applying_residence = models.CharField(max_length=3, choices=YES_NO,
                                             verbose_name="Is your spouse applying for residence in Botswana?", default='No')


    class Meta:
        verbose_name = "Spouse Details"
        verbose_name_plural = "Spouses Details"
