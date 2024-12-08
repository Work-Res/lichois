from django.db import models
from base_module.choices import YES_NO


class InvestorModelMixin(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    services_offered = models.TextField(null=True, blank=True)
    capacity_employed = models.IntegerField(null=True, blank=True)
    draw_salary = models.BooleanField(choices=YES_NO, null=True, blank=True)
    reason_draw_salary = models.TextField(null=True, blank=True)
    salary_per_annum = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    reasons_capacity_employed = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "workresidentpermit"
        abstract = True
