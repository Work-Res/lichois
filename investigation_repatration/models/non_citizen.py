from django.db import models

from django_countries.fields import CountryField


class NonCitizen(models.Model):

    first_name = models.CharField(
        max_length=250, verbose_name='First Name')

    middle_name = models.CharField(
        max_length=250, verbose_name='Middle Name')

    last_name = models.CharField(
        max_length=250, verbose_name='Last Name')

    passport_number = models.CharField(
        max_length=50, unique=True,
        verbose_name='Passport Number')

    country = CountryField(
        verbose_name='Country of Origin')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.passport_number}"
