from django.db import models
from app.models import ApplicationBaseModel
from django.core.validators import MaxLengthValidator


class SeasonalFarmWorker(ApplicationBaseModel):
    nature_of_work_needed = models.CharField(max_length=255, verbose_name="Nature of Seasonal Farm Work Needed")
    occupation = models.CharField(max_length=255, verbose_name="Occupation")
    period_for_work_activity = models.CharField(
        max_length=100,
        verbose_name="Period for seasonal farm work activity",
        validators=[
            MaxLengthValidator(7, message="The period for work activity must not exceed 6 months.")
        ]
    )
    job_requirements = models.TextField(verbose_name="Job Requirements")
    remuneration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Remuneration")
    employer_name = models.CharField(max_length=255, verbose_name="Employer/Business Name")
    farm_address = models.CharField(max_length=255, verbose_name="Business/Farm address including physical (Farm location)")
    farm_type_of_products = models.CharField(max_length=255, verbose_name="Type of farm products")
