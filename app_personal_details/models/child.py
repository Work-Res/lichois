from django.db import models
from app.models import ApplicationBaseModel

from ..choices import GENDER
from base_module.choices import YES_NO


class Child(ApplicationBaseModel):

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    dob = models.DateField(null=True, blank=True)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=6, choices=GENDER)

    is_applying_residence = models.CharField(max_length=3, choices=YES_NO)

    is_adult = models.BooleanField(default=False)

    is_minor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
