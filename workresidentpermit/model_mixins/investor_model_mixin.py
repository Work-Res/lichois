from django.db import models
from base_module.choices import YES_NO


class InvestorModelMixin(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name of Company')
    address = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True, verbose_name='Tel NO')
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name='Location of company/business(i.e'
                                                                                    'plot no. and town/village name)')
    services_offered = models.TextField(
        null=True,
        blank=True,
        verbose_name='What services/products does your company provide'
    )
    capacity_employed = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Capacity in which you will be employed'
    )
    draw_salary = models.BooleanField(
        choices=YES_NO,
        null=True,
        blank=True,
        verbose_name='Will you draw salary? Yes/No'
    )
    reason_draw_salary = models.TextField(
        null=True,
        blank=True,
        verbose_name=''
    )
    salary_per_annum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='If yes state salary per annum'
    )
    reasons_capacity_employed = models.TextField(
        null=True,
        blank=True,
        verbose_name='If no explain why'
    )

    class Meta:
        app_label = "workresidentpermit"
        abstract = True
