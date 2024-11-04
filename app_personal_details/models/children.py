from django.db import models
from app.models import ApplicationBaseModel

from ..choices import GENDER
from base_module.choices import YES_NO


class Children(ApplicationBaseModel):

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=6, choices=GENDER)

    is_applying_residence = models.CharField(max_length=3, choices=YES_NO)

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
