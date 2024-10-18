from django.db import models
from app.models import ApplicationBaseModel


class Country_of_residence(ApplicationBaseModel):

    country = models.CharField(max_length=150)

    period_from = models.CharField(max_length=150)

    period_until = models.CharField(max_length=150)


    class Meta:
        verbose_name = "Country of residence"
        verbose_name_plural = "Coutries of residence"
