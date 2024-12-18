from django.db import models
from app.models import ApplicationBaseModel

from ..choices import GENDER
from base_module.choices import YES_NO


class Child(ApplicationBaseModel):

    first_name = models.CharField(max_length=150, verbose_name="First Name")

    last_name = models.CharField(max_length=150, verbose_name="Last Name")

    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")

    age = models.PositiveIntegerField(verbose_name="Age")

    gender = models.CharField(max_length=6, choices=GENDER, verbose_name="Sex")

    is_applying_residence = models.CharField(max_length=3, choices=YES_NO, verbose_name="Whether applying For Residence")

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
